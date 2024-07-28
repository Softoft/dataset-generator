import json
import logging
import time

from ai.chat_assistant_analysis import AssistantAnalyzer
from graph.graph_ticket_generator import GraphTicketGenerator


class TicketGenerator:
    def __init__(self, dataset_size, output_file, batch_size):
        self.graph_ticket_generator = GraphTicketGenerator()
        self.dataset_size = dataset_size
        self.output_file = output_file
        self.amount_batches = dataset_size // batch_size
        self.batch_size = batch_size

    async def generate_dataset(self):
        results = []
        for i in range(self.amount_batches):
            results.extend(await self._generate_batch_of_tickets())
        return results

    def _save_dataset(self, dataset: list[dict]):
        json.dump(dataset, open(self.output_file, "w", encoding="utf-8"))
        logging.warning(f"Saved {len(dataset)} tickets to {self.output_file}")

    async def _generate_batch_of_tickets(self):
        results = []
        for i in range(self.batch_size):
            tickets_list = await self._get_tickets_as_dict_list()
            results.extend(tickets_list)
            self._save_dataset(results)
        return results

    async def _get_tickets_as_dict_list(self) -> list[dict]:
        ticket_generation_graph = GraphTicketGenerator()
        tickets = await ticket_generation_graph.create_translated_tickets()
        return [ticket.to_dict() for ticket in tickets]

    def _log_dataset_generation_status(self, current_batch_number, start_time: float):
        batches_finished = current_batch_number + 1
        time_passed = time.time() - start_time
        time_per_batch = time_passed / batches_finished
        time_left_s = round(time_per_batch * (self.amount_batches - batches_finished))
        time_left_m = time_left_s // 60

        logging.warning("=" * 50)
        logging.warning(f"Did {batches_finished} Batches in {round(time_passed)}s")
        logging.warning(f"time left: {time_left_s}s = {time_left_m}m")
        expected_total_cost = self.dataset_size * AssistantAnalyzer().calculate_average_cost()
        logging.warning(f"Expected total cost: {round(expected_total_cost, 2)}€")
