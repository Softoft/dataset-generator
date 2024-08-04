import pytest
from graph.graph_ticket_generator import GraphTicketGenerator

from synthetic_data_generator.ai_graph.data.models import TicketEmail


@pytest.mark.expensive
@pytest.mark.asyncio
async def test_ticket_email_generator_node():
    ticket_email_generator_node = GraphTicketGenerator().ticket_email_generator_node
    shared_storage = await ticket_email_generator_node.execute()
    ticket_email = shared_storage.get(TicketEmail)
    print(ticket_email)
