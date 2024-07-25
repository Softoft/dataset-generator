import asyncio

from graph.graph import Graph
from graph.data.priority import Priority
from graph.data.queue import TicketQueue
from graph.data.ticket_type import TicketType


def test_random_priority_node():
    ticket_queue_priority_node = Graph().ticket_queue_priority_node
    shared_storage = ticket_queue_priority_node.execute()
    assert shared_storage.load(TicketQueue) is not None
    assert shared_storage.load(Priority) is not None
    assert shared_storage.load(TicketType) is not None
