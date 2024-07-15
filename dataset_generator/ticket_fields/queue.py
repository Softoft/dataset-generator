import enum

from dataset_generator.ticket_fields.random_collection import IRandomCollection, RandomCollection


class Queue(enum.Enum):
    SOFTWARE = "Software"
    HARDWARE = "Hardware"
    ACCOUNTING = "Accounting"


random_queue_collection: IRandomCollection = RandomCollection.from_value_list(list(Queue))
