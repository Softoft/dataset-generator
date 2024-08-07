import pytest

from models import Ticket


@pytest.mark.expensive
@pytest.mark.asyncio
async def test_creating_ticket_works(create_answer_ticket_node):
    ticket_answer_node = create_answer_ticket_node()
    shared_storage = await ticket_answer_node.execute()

    ticket = shared_storage.get(Ticket)
    assert ticket is not None
    print(ticket)
