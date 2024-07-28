import asyncio

import pytest

from graph.data.models import TicketExtraInformation


@pytest.mark.expensive
@pytest.mark.asyncio
async def test_extra_information_node(create_extra_ticket_information_node):
    extra_ticket_information_node = create_extra_ticket_information_node()
    shared_storage = await extra_ticket_information_node.execute()
    extra_ticket_information = shared_storage.get(TicketExtraInformation)
    assert extra_ticket_information is not None
