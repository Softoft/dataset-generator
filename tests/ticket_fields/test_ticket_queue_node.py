import asyncio

from graph.graph import Graph
from graph.data.ticket_queue import TicketQueue
from graph.data.ticket_type import TicketType


def test_random_queue_node():
    ticket_queue_node = Graph().ticket_queue_node
    shared_storage = ticket_queue_node.execute()
    assert shared_storage.load(TicketQueue) is not None
    assert shared_storage.load(TicketType) is not None
