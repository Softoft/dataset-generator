import asyncio
import json
import logging
import time
import random

from src.ticket import get_random_ticket
from prompt_generation.prompt_generator import PromptGenerator, TextLengthGenerator
from ai.chat_assistant import ChatAssistant

ASSISTANT_ID = "asst_015ugl1zMDzfMHCBVfZxnCW4"
GPT_TEMPERATURE = 1.25


class DatasetGeneratorBuilder:
    def __init__(self, dataset_size, output_file, batch_size):
        self.dataset_size = dataset_size
        self.output_file = output_file
        self.batch_size = batch_size
        self.text_length_mean = 300
        self.text_length_stddev_factor = 1.5
        self.text_length_stddev = None
        self.text_length_min = 20
        self.text_length_max = 10 ** 5
        self.text_length_diff = 30

    def build(self):
        if self.text_length_stddev is None:
            self.text_length_stddev = self.text_length_mean * self.text_length_stddev_factor
        self.text_length_mean += random.uniform(-self.text_length_mean / 10, self.text_length_mean / 10)
        text_length_generator = TextLengthGenerator(self.text_length_mean, self.text_length_stddev,
                                                    self.text_length_min, self.text_length_max, self.text_length_diff)
        prompt_generator = PromptGenerator(text_length_generator)
        return DatasetGenerator(self.dataset_size, self.output_file, self.batch_size, prompt_generator)


class DatasetGenerator:
    def __init__(self, dataset_size, output_file, batch_size, prompt_generator: PromptGenerator):
        self.prompt_generator = prompt_generator
        self.dataset_size = dataset_size
        self.output_file = output_file
        self.amount_batches = dataset_size // batch_size
        self.batch_size = batch_size
        self.assistant = ChatAssistant(ASSISTANT_ID, temperature=GPT_TEMPERATURE)

    async def get_ticket_as_dict(self) -> dict:
        ticket = get_random_ticket()
        prompt = self.prompt_generator.create_prompt(ticket)
        logging.info(f"Prompt: {prompt}")
        raw_response = await self.assistant.chat_assistant(prompt)

        try:
            response = json.loads(raw_response)
            if "subject" not in response or "text" not in response:
                logging.error(f"Invalid response: {response}")
                return {}
            ticket.subject = response["subject"]
            ticket.text = response["text"]
            return ticket.to_dict()
        except json.JSONDecodeError:
            logging.error(f"Error decoding JSON: {raw_response}")
            return {}

    def save_dataset(self, dataset: list[dict], file_path):
        json.dump(dataset, open(file_path, "w", encoding="utf-8"))
        logging.warning(f"Saved {len(dataset)} tickets to {file_path}")

    def log_dataset_generation_status(self, current_batch_number, start_time: float):
        batches_finished = current_batch_number + 1
        time_passed = time.time() - start_time
        time_per_batch = time_passed / batches_finished
        time_left = time_per_batch * (self.amount_batches - batches_finished)
        time_left_s = round(time_left)
        time_left_m = time_left_s // 60
        logging.warning("=" * 50)
        logging.warning(f"Did {batches_finished} Batches in {round(time_passed)}s")
        logging.warning(f"time left: {time_left_s}s = {time_left_m}m")
        expected_total_cost = self.dataset_size * self.assistant.assistant_analysis.calculate_average_cost()
        logging.warning(f"Expected total cost: {round(expected_total_cost, 2)}€")

    async def generate_dataset(self):
        start_time = time.time()

        results = []
        for i in range(self.amount_batches):
            try:
                tasks = [self.get_ticket_as_dict() for _ in range(self.batch_size)]
                results.extend(await asyncio.gather(*tasks))
                self.save_dataset(results, self.output_file)
                self.log_dataset_generation_status(i, start_time)
            except Exception as e:
                logging.error(f"Error in batch {i}: {e}")
                await asyncio.sleep(60)
        return results
