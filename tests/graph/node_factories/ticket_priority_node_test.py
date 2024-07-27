import asyncio

from graph.graph_ticket_generator import GraphTicketGenerator
from graph.data.models import Priority, TicketQueue, TicketType


def test_random_priority_node():
    ticket_queue_priority_node = GraphTicketGenerator().ticket_queue_priority_node
    shared_storage = asyncio.run(ticket_queue_priority_node.execute())
    assert shared_storage.load(TicketQueue) is not None
    assert shared_storage.load(Priority) is not None
    assert shared_storage.load(TicketType) is not None
