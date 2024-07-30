import asyncio
import json
import logging
import time
from typing import Callable

from injector import inject

from ai.chat_assistant_analysis import AssistantAnalyzer
from config import Config
from graph.graph_ticket_generator import GraphTicketGenerator


class TicketGenerator:
    @inject
    def __init__(self, ticket_generation_config: Config,
                 create_ticket_generator: Callable[[], GraphTicketGenerator]):
        self.create_ticket_generator = create_ticket_generator
        self.number_translation_nodes = ticket_generation_config.number_translation_nodes
        self.number_of_tickets = ticket_generation_config.number_of_tickets
        self.graph_ticket_runs = self.number_of_tickets // self.number_translation_nodes
        self.output_file = ticket_generation_config.output_file
        self.batch_size_in_graph_runs = ticket_generation_config.batch_size
        self.amount_batches = int(
            (self.number_of_tickets / self.batch_size_in_graph_runs) / self.number_translation_nodes)
        self.__check_output_file_doesnt_exist()

    def __check_output_file_doesnt_exist(self):
        try:
            open(self.output_file)
            logging.warning(f"File {self.output_file} already exists. Do you want to overwrite it?[y]/n")
            if input() == "n":
                raise FileExistsError(f"File {self.output_file} already exists")

        except FileNotFoundError:
            pass

    async def generate_dataset(self):
        results = []
        start_time = time.time()
        for i in range(self.amount_batches):
            results.extend(await self._generate_batch_of_tickets())
            self._save_dataset(results)
            self._log_dataset_generation_status(i, start_time, len(results))
        return results

    def _save_dataset(self, dataset: list[dict]):
        json.dump(dataset, open(self.output_file, "w", encoding="utf-8"))
        logging.warning(f"Saved {len(dataset)} tickets to {self.output_file}")

    async def _generate_batch_of_tickets(self):
        ticket_list_tasks = []
        for i in range(self.batch_size_in_graph_runs):
            ticket_list_tasks.append(self._get_tickets_as_dict_list())

        ticket_list_of_lists = await asyncio.gather(*ticket_list_tasks)
        results = []
        for result in ticket_list_of_lists:
            results.extend(result)
        return results

    async def _get_tickets_as_dict_list(self) -> list[dict]:
        ticket_generation_graph = self.create_ticket_generator()
        try:
            tickets = await ticket_generation_graph.create_translated_tickets()
            return [ticket.to_dict() for ticket in tickets]
        except Exception as e:
            logging.error(f"Error while generating tickets: {e}")
            return []

    def _log_dataset_generation_status(self, current_batch_number, start_time: float, created_tickets: int):
        batches_finished = current_batch_number + 1
        time_passed = time.time() - start_time
        time_per_batch = time_passed / batches_finished
        time_left_s = round(time_per_batch * (self.amount_batches - batches_finished))
        time_left_m = time_left_s // 60

        logging.warning("=" * 50)
        logging.warning(f"Did {batches_finished} Batches in {round(time_passed)}s")
        logging.warning(f"time left: {time_left_s}s = {time_left_m}m")
        costs = AssistantAnalyzer.get_instance().calculate_total_cost()
        cost_per_ticket = costs / created_tickets if created_tickets > 0 else 0
        logging.warning(f"Costs per Ticket: {round(cost_per_ticket, 4)}€")
        logging.warning(f"Total Costs: {round(costs, 2)}€")
        AssistantAnalyzer.get_instance().generate_cost_summary()
