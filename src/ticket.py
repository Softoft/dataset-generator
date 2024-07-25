import dataclasses
from enum import Enum

from graph.data.language import Language, random_language_collection
from graph.data.priority import Priority, random_priority_collection
from graph.data.queue import Queue, random_queue_collection
from src.ticket_fields.subcategory import SubCategoryRandomCollection


def get_random_ticket():
    queue = random_queue_collection.get_random_value()
    return Ticket(
        queue=queue,
        priority=random_priority_collection.get_random_value(queue),
        language=random_language_collection.get_random_value(),
        subcategory=SubCategoryRandomCollection().get_random_value(queue),
    )


@dataclasses.dataclass
class Ticket:
    queue: Queue
    priority: Priority
    language: Language
    subcategory: str
    subject: str = ""
    text: str = ""

    def to_dict(self):
        def serialize(obj):
            if isinstance(obj, Enum):
                return obj.name
            return obj

        return {k: serialize(v) for k, v in dataclasses.asdict(self).items()}
