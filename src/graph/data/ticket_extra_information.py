from dataclasses import dataclass


@dataclass
class TicketExtraInformation:
    topic: str
    product_category: str
    product: str
