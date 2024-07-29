import json
import logging
import time
from dataclasses import dataclass

from ai.chat_assistant_analysis import AssistantAnalyzer
from graph.graph_ticket_generator import GraphTicketGenerator
from graph.nodes.ticket_rewriting_and_translating_node import TextSimilarityThresholds


@dataclass
class TicketGenerationConfig:
    number_of_tickets: int
    output_file: str
    number_translation_nodes: int
    mean_text_length: int
    text_length_standard_deviation: int
    batch_size: int
    text_similarity_thresholds: TextSimilarityThresholds


class TicketGenerator:
    def __init__(self, ticket_generation_config: TicketGenerationConfig):
        self.ticket_generation_config = ticket_generation_config
        self.number_translation_nodes = ticket_generation_config.number_translation_nodes
        self.number_of_tickets = ticket_generation_config.number_of_tickets
        self.graph_ticket_runs = self.number_of_tickets // self.number_translation_nodes
        self.output_file = ticket_generation_config.output_file
        self.batch_size_in_graph_runs = ticket_generation_config.batch_size
        self.amount_batches = self.number_of_tickets // self.batch_size_in_graph_runs // self.number_translation_nodes
        self.__check_output_file_doesnt_exist()

    def __check_output_file_doesnt_exist(self):
        try:
            open(self.output_file)
            logging.error(f"File {self.output_file} already exists. Please delete it first.")
            exit(1)
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
        results = []
        for i in range(self.batch_size_in_graph_runs):
            tickets_list = await self._get_tickets_as_dict_list()
            results.extend(tickets_list)
        return results

    async def _get_tickets_as_dict_list(self) -> list[dict]:
        ticket_generation_graph = GraphTicketGenerator(self.ticket_generation_config)
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
        cost_per_ticket = costs / created_tickets
        logging.warning(f"Costs per Ticket: {round(cost_per_ticket, 4)}€")
        logging.warning(f"Total Costs: {round(costs, 2)}€")
        AssistantAnalyzer.get_instance().generate_cost_summary()
