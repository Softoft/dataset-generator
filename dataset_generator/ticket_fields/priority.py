import enum

from dataset_generator.ticket_fields.random_collection import IRandomCollection, RandomCollection
from dataset_generator.ticket_fields.queue import Queue


class Priority(enum.Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class PriorityCollection(IRandomCollection):
    def __init__(self):
        self.queue_priority_mapping = {
            Queue.SOFTWARE:
                RandomCollection({Priority.LOW: 1, Priority.MEDIUM: 1, Priority.HIGH: 2}),
            Queue.HARDWARE:
                RandomCollection({Priority.LOW: 1, Priority.MEDIUM: 2, Priority.HIGH: 1}),
            Queue.ACCOUNTING:
                RandomCollection({Priority.LOW: 1, Priority.MEDIUM: 2, Priority.HIGH: 1})
        }

    def get_random_value(self, queue, **kwargs) -> Priority:
        return self.queue_priority_mapping[queue].get_random_value()


random_priority_collection: IRandomCollection = PriorityCollection()
