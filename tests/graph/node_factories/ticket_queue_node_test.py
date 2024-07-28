import asyncio

from graph.graph_ticket_generator import GraphTicketGenerator
from graph.data.models import TicketQueue, TicketType


def test_random_queue_node():
    ticket_queue_node = GraphTicketGenerator().ticket_queue_node
    shared_storage = asyncio.run(ticket_queue_node.execute())
    assert shared_storage.get(TicketQueue) is not None
    assert shared_storage.get(TicketType) is not None
