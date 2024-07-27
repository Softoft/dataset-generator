import asyncio

import pytest

from graph.data.models import Ticket


@pytest.mark.expensive
def test_creating_ticket_works(create_answer_ticket_node):
    ticket_answer_node = create_answer_ticket_node()
    shared_storage = asyncio.run(ticket_answer_node.execute())

    ticket = shared_storage.load(Ticket)
    assert ticket is not None
    print(ticket)
