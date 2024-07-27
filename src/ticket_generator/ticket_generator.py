import asyncio
import dataclasses
import json
import logging
import time

from graph.graph_ticket_generator import GraphTicketGenerator


class TicketGenerator:
    def __init__(self, dataset_size, output_file, batch_size):
        self.dataset_size = dataset_size
        self.output_file = output_file
        self.amount_batches = dataset_size // batch_size
        self.batch_size = batch_size

    def save_dataset(self, dataset: list[dict], file_path):
        json.dump(dataset, open(file_path, "w", encoding="utf-8"))
        logging.warning(f"Saved {len(dataset)} tickets to {file_path}")

    async def generate_dataset(self):
        results = []
        for i in range(self.amount_batches):
            try:
                tasks = [self.get_ticket_as_dict() for _ in range(self.batch_size)]
                results.extend(await asyncio.gather(*tasks))
                self.save_dataset(results, self.output_file)
            except Exception as e:
                logging.error(f"Error in batch {i}: {e}")
        return results

    async def get_ticket_as_dict(self) -> dict:
        ticket_generation_graph = GraphTicketGenerator()
        ticket = await ticket_generation_graph.create_translated_ticket()
        return ticket.to_dict()
