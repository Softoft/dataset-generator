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

    def _save_dataset(self, dataset: list[dict], file_path):
        json.dump(dataset, open(file_path, "w", encoding="utf-8"))
        logging.warning(f"Saved {len(dataset)} tickets to {file_path}")

    async def _generate_batch_of_tickets(self):
        results = []
        for i in range(self.batch_size):
            try:
                ticket_dict = await self._get_ticket_as_dict()
                results.append(ticket_dict)
            except Exception as e:
                logging.error(f"Error in batch {i}: {e}")
        return results

    async def _get_ticket_as_dict(self) -> dict:
        ticket_generation_graph = GraphTicketGenerator()
        ticket = await ticket_generation_graph.create_translated_ticket()
        return ticket.to_dict()

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
