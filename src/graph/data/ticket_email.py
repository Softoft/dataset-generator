from dataclasses import dataclass


@dataclass
class TicketEmail:
    subject: str
    body: str
