import asyncio

from graph.graph_ticket_generator import GraphTicketGenerator

from synthetic_data_generator.ai_graph.data.models import Priority, TicketQueue, TicketType


def test_random_priority_node():
    ticket_queue_priority_node = GraphTicketGenerator().ticket_queue_priority_node
    shared_storage = asyncio.run(ticket_queue_priority_node.execute())
    assert shared_storage.get(TicketQueue) is not None
    assert shared_storage.get(Priority) is not None
    assert shared_storage.get(TicketType) is not None
