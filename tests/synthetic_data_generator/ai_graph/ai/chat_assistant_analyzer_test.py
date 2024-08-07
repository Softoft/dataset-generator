import asyncio
import logging

import pytest

from synthetic_data_generator.ai_graph.ai.chat_assistant_analysis import AssistantAnalysisResult, AssistantRun,\
    AssistantRuns
from synthetic_data_generator.ai_graph.ai.chat_assistant_config import AssistantModel


@pytest.mark.parametrize("prompt_tokens,completion_tokens,model,expected_cost", [
    (1e6, 2e6, AssistantModel.GPT_4o, 35),
    (2e6, 1e6, AssistantModel.GPT_4o, 25),
    (2e6, 1e6, AssistantModel.GPT_4o_MINI, 0.9),

])
def test_assistant_run(create_assistant_run, prompt_tokens, completion_tokens, model, expected_cost):
    assistant_run: AssistantRun = create_assistant_run(assistant_name="Test", prompt_tokens=prompt_tokens,
                                                       completion_tokens=completion_tokens, model=model)
    cost = assistant_run.cost
    assert cost == pytest.approx(expected_cost)


def test_assistant_run_composite(create_mocked_assistant_run):
    assistant_run_1 = create_mocked_assistant_run(1e6, 2e6, 100)
    assistant_run_2 = create_mocked_assistant_run(2e6, 1e6, 200)
    assistant_runs = AssistantRuns(_runs=[assistant_run_1, assistant_run_2])
    assert assistant_runs.cost == 300
    assert assistant_runs.prompt_tokens == 3e6
    assert assistant_runs.completion_tokens == 3e6


def test_assistant_analysis_result():
    assistant_analysis_result = AssistantAnalysisResult(name="Test",
                                                        cost=100,
                                                        total_cost=1000,
                                                        prompt_tokens=int(1e6),
                                                        completion_tokens=int(2e6)
                                                        )
    assert assistant_analysis_result.cost == 100
    assert assistant_analysis_result.total_cost == 1000
    assert assistant_analysis_result.percent_total_cost == 10
    assert assistant_analysis_result.prompt_tokens == 1e6
    assert assistant_analysis_result.completion_tokens == 2e6

    assert all([text in str(assistant_analysis_result).lower() for text in ["cost", "100", "10"]])


def test_assistant_analyzer_total_summary(create_mocked_assistant_run, chat_assistant_analyzer):
    assistant_run_1 = create_mocked_assistant_run(1e6, 2e6, 100)
    assistant_run_2 = create_mocked_assistant_run(2e6, 1e6, 200)

    chat_assistant_analyzer.append_assistant_run(assistant_run_1)
    chat_assistant_analyzer.append_assistant_run(assistant_run_2)

    assert chat_assistant_analyzer.total_summary().cost == 300
    assert chat_assistant_analyzer.total_summary().prompt_tokens == 3e6
    assert chat_assistant_analyzer.total_summary().completion_tokens == 3e6


def test_print_assistant_analyzer(create_mocked_assistant_run, chat_assistant_analyzer):
    assistant_run_1 = create_mocked_assistant_run(1e6, 2e6, 100)
    assistant_run_2 = create_mocked_assistant_run(2e6, 1e6, 200)

    chat_assistant_analyzer.append_assistant_run(assistant_run_1)
    chat_assistant_analyzer.append_assistant_run(assistant_run_2)

    assistant_analyzer_text = str(chat_assistant_analyzer)
    assert all([text in assistant_analyzer_text.lower() for text in ["cost", "300"]])


@pytest.mark.asyncio
@pytest.mark.slow
async def test_chat_assistant_analyzer(chat_assistant_gpt4_o_mini, chat_assistant_analyzer):
    await chat_assistant_gpt4_o_mini.get_response("What is the capital of Germany?")
    logging.info(chat_assistant_analyzer)
    assert chat_assistant_analyzer.total_summary().cost == pytest.approx(0, abs=0.1)
    assert 30 < chat_assistant_analyzer.total_summary().prompt_tokens < 60
    assert 0 < chat_assistant_analyzer.total_summary().completion_tokens < 40


@pytest.mark.asyncio
@pytest.mark.slow
async def test_chat_assistant_analyzer_get_by_name(create_chat_assistant, chat_assistant_analyzer):
    ASSISTANT_NAME1 = "Test1"
    assistant1 = create_chat_assistant(assistant_name=ASSISTANT_NAME1, model=AssistantModel.GPT_4o_MINI,
                                       instructions="Answer a question in one word!")
    ASSISTANT_NAME2 = "Test2"
    assistant2 = create_chat_assistant(assistant_name=ASSISTANT_NAME2, model=AssistantModel.GPT_4o_MINI,
                                       instructions="Answer this question, short", temperature=1)

    tasks = [assistant1.get_response("What is the capital of Germany?"),
             assistant2.get_response("Is C# a programming language?"),
             assistant2.get_response("What Programming Language is the pytest lib from?"), ]

    await asyncio.gather(*tasks)
    summary1 = chat_assistant_analyzer.get_summary_for_assistant(ASSISTANT_NAME1)
    summary2 = chat_assistant_analyzer.get_summary_for_assistant(ASSISTANT_NAME2)

    assert summary1.prompt_tokens > 0
    assert summary1.completion_tokens > 0
    assert summary1.prompt_tokens < summary2.prompt_tokens
    assert summary1.completion_tokens < summary2.completion_tokens
    assert summary1.cost < summary2.cost
