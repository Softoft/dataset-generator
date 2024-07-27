import pytest

from graph.data.models import TicketEmail
from graph.graph import Graph


@pytest.mark.expensive
def test_ticket_email_generator_node():
    ticket_email_generator_node = Graph().ticket_email_generator_node
    shared_storage = ticket_email_generator_node.execute()
    ticket_email = shared_storage.load(TicketEmail)
    print(ticket_email)
