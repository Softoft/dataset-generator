import asyncio

import pytest

from graph.data.models import Priority, TicketExtraInformation, TicketQueue, TicketType
from util.key_value_storage import KeyValueStore


@pytest.mark.expensive
def test_extra_information_node(create_key_value_store, extra_ticket_information_node):
    key_value_store = create_key_value_store(TicketType.PROBLEM, TicketQueue.IT_SUPPORT, Priority.HIGH)

    shared_storage: KeyValueStore = asyncio.run(extra_ticket_information_node.execute(key_value_store))
    assert shared_storage.get(TicketExtraInformation) is not None
