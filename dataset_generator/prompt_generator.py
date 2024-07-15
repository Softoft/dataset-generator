import dataclasses

import numpy as np

from dataset_generator.ticket import Ticket
from dataset_generator.ticket_fields.priority import Priority
from dataset_generator.ticket_fields.queue import Queue

rng = np.random.default_rng(seed=42)

PRIORITY_HIGH_TEXT = """
Die Priorität ist hoch, das bedeutet:
Wenn jemand gehackt wurde, sein Gerät sich nicht einschalten lässt, er das Gerät/Software aber braucht.
Wenn er das Gerät/Software nicht verwenden kann, aus unterschiedlichen Gründen, er es aber braucht.
Wenn jemand unbedingt eine Rechnung benötigt, aus verschiedenen Gründen,
Falls ein Kunde ein Security Update, gegen eine ernstzunehmende Sicherheitslücke gefunden hat.
"""

PRIORITY_MEDIUM_TEXT = """
Die Priorität ist mittel/normal, das bedeutet:
sind normale Standard Probleme, die nicht direkt erledigt werden müssen und keinen starken Effekt haben.
Kunde braucht Update auf neue Software Version. Dem Kunden ist ein Bug aufgefallen. Sein Gerät hat einen kleinen Fehler.
Braucht eine Rechnung. Neuer Kunde will ein Angebot für eine Software Entwicklung haben.
Ein bestehender Kunde hat sich beschwert, dass seine Emails nicht beantwortet wurde.Kunde hat sich beschwert.
"""

PRIORITY_LOW_TEXT = """
Die Priorität ist niedrig, das bedeutet:
Das Ticket ist unwichtig, es besteht wenig Zeitdruck:
Es ist ein kleiner Fehler in der verwendeten Software oder Hardware aufgefallen.
Frage ob seine nächste Rechnung, einen anderen Unternehmensname angeben kann.
Frage ob er ein Angebot haben kann, aber er hat es nicht eilig oder braucht es nicht wirklich.
Ein Kunde gibt positives Feedback, ohne konkreten Handlungsbedarf
Kunde schreibt, dass er für sein System vielleicht ein Update gebrauchen könnte.
Kunde fragt, ob er für eine Rechnung eine kleine Änderung bekommen kann
"""


@dataclasses.dataclass(frozen=True)
class TextLengthGenerator:
    mean: int
    std_dev: int
    lower_bound: int = 50
    upper_bound: int = 500
    upper_text_length_diff: int = 30

    def is_in_bound(self, number: float | int):
        return self.lower_bound < number < self.upper_bound

    def generate_number(self):
        return rng.normal(self.mean, self.std_dev)

    def generate_text_length_bounds(self):
        number = self.generate_number()
        while not self.is_in_bound(number):
            number = self.generate_number()
        return int(number), int(number + self.upper_text_length_diff)


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
        match priority:
            case Priority.LOW:
                return PRIORITY_LOW_TEXT
            case Priority.MEDIUM:
                return PRIORITY_MEDIUM_TEXT
            case Priority.HIGH:
                return PRIORITY_HIGH_TEXT
            case _:
                raise ValueError("Invalid Priority")
