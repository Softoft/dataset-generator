import dataclasses
import logging
import math

import numpy as np

from dataset_generator.prompt_generation.prompt_priority_texts import get_priorities_prompt
from dataset_generator.ticket import Ticket
from dataset_generator.ticket_fields.priority import Priority
from dataset_generator.ticket_fields.queue import Queue

rng = np.random.default_rng(seed=42)


@dataclasses.dataclass(frozen=True)
class TextLengthGenerator:
    mean: int
    std_dev: int
    lower_bound: int = 30
    upper_bound: int = 10 ** 5
    min_text_length_diff: int = 15

    def __post_init__(self):
        assert self.is_in_bound(self.mean), "Mean is out of bounds"
        assert self.lower_bound >= 0
        if self.lower_bound <= 10:
            logging.warning("Bound lower than 10 could lead to extremely short messages"
                            )

    def is_in_bound(self, number: float | int):
        return self.lower_bound < number < self.upper_bound

    def generate_text_length(self):
        mu = np.log(self.mean ** 2 / np.sqrt(self.std_dev ** 2 + self.mean ** 2))
        sigma = np.sqrt(np.log(1 + (self.std_dev ** 2 / self.mean ** 2)))
        return int(np.random.lognormal(mu, sigma))

    def generate_upper_text_length(self, text_length: int):
        return text_length + math.log(text_length) * self.min_text_length_diff

    def generate_text_length_bounds(self):
        text_length = self.generate_text_length()
        while not self.is_in_bound(text_length):
            text_length = self.generate_text_length()
        return text_length, self.generate_upper_text_length(text_length)


class PromptGenerator:
    def __init__(self, text_length_generator: TextLengthGenerator):
        self.text_length_generator = text_length_generator

    def create_prompt(self, ticket: Ticket):
        text_length_min, text_length_max = self.text_length_generator.generate_text_length_bounds()

        return (
            f"Generiere ein Ticket; Für die Queue: {ticket.queue}; "
            f"{self.generate_priority_extra_information(ticket.priority)};"
            f"{self.generate_subcategory_extra_information(ticket.queue, ticket.subcategory)};"
            f" Der Ticket Text muss eine Länge zwischen {text_length_min} und {text_length_max} Zeichen haben."
            f" Die Sprache des Tickets ist {ticket.language.value};")

    def generate_subcategory_extra_information(self, queue: Queue, subcategory: str):
        match queue:
            case Queue.SOFTWARE:
                return f"Der Kunde verwendet die Software {subcategory};"
            case Queue.HARDWARE:
                return f"Der Kunde verwendet die Hardware {subcategory};"
            case Queue.ACCOUNTING:
                return f"Es geht um {subcategory};"
            case _:
                raise ValueError("Invalid Queue")

    def generate_priority_extra_information(self, priority: Priority):
        return get_priorities_prompt(priority)
