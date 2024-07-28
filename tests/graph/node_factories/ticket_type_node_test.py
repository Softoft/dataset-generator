import asyncio

from graph.graph_ticket_generator import GraphTicketGenerator
from graph.data.models import TicketType


def test_random_ticket_type():
    ticket_type_node = GraphTicketGenerator().ticket_type_node
    shared_storage = asyncio.run(ticket_type_node.execute())
    assert shared_storage.get(TicketType) is not None
