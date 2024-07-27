import asyncio

import pytest

from graph.data.models import TranslatedTicket


@pytest.mark.expensive
def test_creating_ticket_works(create_ticket_translation_node):
    ticket_translation_node = create_ticket_translation_node()
    shared_storage = asyncio.run(ticket_translation_node.execute())

    ticket = shared_storage.load(TranslatedTicket)
    assert ticket is not None
    print(ticket)
