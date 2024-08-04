import pytest


@pytest.mark.asyncio
@pytest.mark.expensive
async def test_chat_assistant(chat_assistant_gpt4_o_mini):
    response = await chat_assistant_gpt4_o_mini.chat_assistant("What is the capital of Germany?")
    assert "Berlin" in response
