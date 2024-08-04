import pytest

from synthetic_data_generator.ai_graph.ai.chat_assistant import AssistantModel
from synthetic_data_generator.ai_graph.ai.chat_assistant_analysis import AssistantAnalyzer, AssistantRun


def test_assistant_run(create_assistant_run):
    assistant_run: AssistantRun = create_assistant_run(assistant_name="Test", prompt_tokens=10, completion_tokens=20,
                                                       model=AssistantModel.GPT_4o)
    cost = assistant_run.calculate_cost()
    assert cost == pytest.approx(0)


@pytest.mark.asyncio
@pytest.mark.slow
async def test_chat_assistant(chat_assistant_gpt4_o_mini):
    AssistantAnalyzer().clear()
    await chat_assistant_gpt4_o_mini.chat_assistant("What is the capital of Germany?")
    assert len(AssistantAnalyzer().runs) == 1
