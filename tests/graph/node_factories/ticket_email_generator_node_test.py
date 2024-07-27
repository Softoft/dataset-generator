import asyncio

import pytest

from graph.data.models import TicketEmail
from graph.graph_ticket_generator import GraphTicketGenerator


@pytest.mark.expensive
def test_ticket_email_generator_node():
    ticket_email_generator_node = GraphTicketGenerator().ticket_email_generator_node
    shared_storage = asyncio.run(ticket_email_generator_node.execute())
    ticket_email = shared_storage.load(TicketEmail)
    print(ticket_email)
