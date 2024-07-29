import json
import logging
import time

from ai.chat_assistant_analysis import AssistantAnalyzer
from graph.graph_ticket_generator import GraphTicketGenerator


class TicketGenerator:
    def __init__(self, total_number_of_tickets, output_file, number_translation_nodes):
        self.number_translation_nodes = number_translation_nodes
        self.dataset_size = total_number_of_tickets
        self.graph_ticket_runs = total_number_of_tickets // number_translation_nodes
        self.output_file = output_file
        self.batch_size_in_graph_runs = 10
        self.amount_batches = total_number_of_tickets // self.batch_size_in_graph_runs // number_translation_nodes

    async def generate_dataset(self):
        results = []
        start_time = time.time()
        for i in range(self.amount_batches):
            results.extend(await self._generate_batch_of_tickets())
            self._save_dataset(results)
            self._log_dataset_generation_status(i, start_time,  len(results))
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
        ticket_generation_graph = GraphTicketGenerator(self.number_translation_nodes)
        tickets = await ticket_generation_graph.create_translated_tickets()
        return [ticket.to_dict() for ticket in tickets]

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
