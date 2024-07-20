import enum
import random

from dataset_generator.ticket_fields.random_collection import IRandomCollection, RandomCollection


class Queue(enum.Enum):
    SOFTWARE = "Software"
    HARDWARE = "Hardware"
    ACCOUNTING = "Accounting"


random_queue_collection: IRandomCollection = RandomCollection({ Queue.SOFTWARE: 2, Queue.HARDWARE: 1, Queue.ACCOUNTING: 1})
