import dataclasses
import math

import numpy as np

from src.prompt_generation.prompt_priority_texts import get_priorities_prompt
from src.ticket import Ticket
from src.ticket_fields.priority import Priority
from src.ticket_fields.queue import Queue

rng = np.random.default_rng(seed=42)



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
