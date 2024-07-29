import json

import pytest

from ai.chat_assistant import ChatAssistant
from graph.data.models import TicketEmail

EMAIL_GENERATION_ASSISTANT_ID = "asst_015ugl1zMDzfMHCBVfZxnCW4"


@pytest.mark.asyncio
@pytest.mark.expensive
async def test_chat_assistant():
    chat_assistant = ChatAssistant(assistant_name="Test", assistant_id=EMAIL_GENERATION_ASSISTANT_ID)
    response = await chat_assistant.chat_assistant("New Email!")
    email_response = json.loads(response)
    TicketEmail(**email_response)


def test_wrong_email_raises_error():
    wrong_json_string = '{"text": "text"}'

    with pytest.raises(TypeError):
        TicketEmail(**json.loads(wrong_json_string))
