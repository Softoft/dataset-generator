import pytest

from synthetic_data_generator.ai_graph.ai.chat_assistant_analysis import AssistantAnalyzer, AssistantRun, AssistantRuns
from synthetic_data_generator.ai_graph.ai.chat_assistant_config import AssistantModel


@pytest.mark.parametrize("prompt_tokens,completion_tokens,model,expected_cost", [
    (1e6, 2e6, AssistantModel.GPT_4o, 35),
    (2e6, 1e6, AssistantModel.GPT_4o, 25),
    (2e6, 1e6, AssistantModel.GPT_4o_MINI, 0.9),

])
def test_assistant_run(create_assistant_run, prompt_tokens, completion_tokens, model, expected_cost):
    assistant_run: AssistantRun = create_assistant_run(assistant_name="Test", prompt_tokens=prompt_tokens,
                                                       completion_tokens=completion_tokens, model=model)
    cost = assistant_run.cost()
    assert cost == pytest.approx(expected_cost)


def test_assistant_run_composite(create_mocked_assistant_run):
    assistant_run_1 = create_mocked_assistant_run(1e6, 2e6, 100)
    assistant_run_2 = create_mocked_assistant_run(2e6, 1e6, 200)
    assistant_runs = AssistantRuns(runs=[assistant_run_1, assistant_run_2])
    assert assistant_runs.cost == 300
    assert assistant_runs.prompt_tokens == 3e6
    assert assistant_runs.completion_tokens == 3e6


def test_assistant_analyzer_total_cost(create_mocked_assistant_run, chat_assistant_analyzer):
    assistant_run_1 = create_mocked_assistant_run(1e6, 2e6, 100)
    assistant_run_2 = create_mocked_assistant_run(2e6, 1e6, 200)

    chat_assistant_analyzer.append_assistant_run(assistant_run_1)
    chat_assistant_analyzer.append_assistant_run(assistant_run_2)

    assert chat_assistant_analyzer.total_summary().cost == 300


@pytest.mark.asyncio
@pytest.mark.slow
async def test_chat_assistant(chat_assistant_gpt4_o_mini):
    AssistantAnalyzer().clear()
    await chat_assistant_gpt4_o_mini.chat_assistant("What is the capital of Germany?")
    assert len(AssistantAnalyzer().runs) == 1
