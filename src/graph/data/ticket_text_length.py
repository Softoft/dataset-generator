from dataclasses import dataclass

from graph.data.category_ticket_field import InputTicketField


@dataclass
class TicketTextLength(InputTicketField):
    lower_bound: int
    upper_bound: int

    def get_description(self):
        return f"Die Länge des Textes liegt zwischen {self.lower_bound} und {self.upper_bound} Zeichen."

    def __eq__(self, other):
        return self.lower_bound == other.lower_bound and self.upper_bound == other.upper_bound

    def __hash__(self):
        return hash((self.lower_bound, self.upper_bound))