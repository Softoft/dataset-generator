from dataclasses import dataclass

from graph.data.category_ticket_field import InputTicketField


@dataclass
class TicketTextLength(InputTicketField):
    lower_bound: int
    upper_bound: int

    def get_description(self):
        return f"Die Länge des Textes liegt zwischen {self.lower_bound} und {self.upper_bound} Zeichen."
