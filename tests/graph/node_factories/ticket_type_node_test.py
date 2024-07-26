import asyncio

from graph.graph import Graph
from graph.data.ticket_type import TicketType


def test_random_ticket_type():
    ticket_type_node = Graph().ticket_type_node
    shared_storage = ticket_type_node.execute()
    assert shared_storage.load(TicketType) is not None
