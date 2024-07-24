import asyncio
import logging

from openai import AsyncOpenAI
from openai.types.beta import AssistantToolChoiceOptionParam
from openai.types.beta.threads import Run
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)


def get_assistant_input_cost(model):
    return {
        "gpt-4o": 5 / 10 ** 6,
        "gpt-4o-2024-05-13": 5 / 10 ** 6,
        "gpt-3.5-turbo-0125": 0.5 / 10 ** 6,
        "gpt-3.5-turbo-instruct": 1.5 / 10 ** 6,
    }[model]


def get_assistant_output_cost(model):
    return {
        "gpt-4o": 15 / 10 ** 6,
        "gpt-4o-2024-05-13": 15 / 10 ** 6,
        "gpt-3.5-turbo-0125": 1.5 / 10 ** 6,
        "gpt-3.5-turbo-instruct": 2 / 10 ** 6,
    }[model]


class AssistantRun:
    def __init__(self, run: Run):
        self.run = run

    def calculate_cost(self):
        input_cost = get_assistant_input_cost(self.run.model) * self.run.usage.prompt_tokens
        output_cost = get_assistant_output_cost(self.run.model) * self.run.usage.completion_tokens
        return input_cost + output_cost


class AssistantAnalysis:
    def __init__(self):
        self.runs: list[AssistantRun] = []

    def append_run(self, run: Run):
        self.runs.append(AssistantRun(run))

    def calculate_total_cost(self):
        return sum([run.calculate_cost() for run in self.runs])

    def calculate_average_cost(self):
        return self.calculate_total_cost() / len(self.runs)


class ChatAssistant:
    def __init__(self, assistant_id, response_format=None, tool_choice=None, temperature=1):
        self.client = AsyncOpenAI()
        self.assistant_id = assistant_id
        self.loop = asyncio.get_event_loop()
        self.response_format = response_format
        self.tool_choice: AssistantToolChoiceOptionParam = tool_choice if tool_choice else "auto"
        self.temperature = temperature
        self.assistant_analysis = AssistantAnalysis()

    def log_run_status(self, run: Run):
        if run.status != "completed":
            logging.error(f"Run failed with status {run.status} and run {run}")
        if run.usage:
            logging.info(f"Run Usage: {run.usage}")

    @retry(wait=wait_random_exponential(min=1, max=120), stop=stop_after_attempt(10))
    async def create_run_with_retry(self, thread_id, assistant_id):
        return await self.client.beta.threads.runs.create_and_poll(thread_id=thread_id,
                                                                   assistant_id=assistant_id,
                                                                   temperature=self.temperature,
                                                                   response_format=self.response_format,
                                                                   tool_choice=self.tool_choice)

    @retry(wait=wait_random_exponential(min=1, max=120), stop=stop_after_attempt(10))
    async def chat_assistant(self, prompt) -> str:
        my_updated_assistant = await self.client.beta.assistants.retrieve(self.assistant_id)
        thread = await self.client.beta.threads.create()

        await self.client.beta.threads.messages.create(thread_id=thread.id, role="user", content=prompt)
        run = await self.create_run_with_retry(thread.id, my_updated_assistant.id)
        self.log_run_status(run)
        self.assistant_analysis.append_run(run)
        messages = await self.client.beta.threads.messages.list(thread_id=thread.id)
        return messages.data[0].content[0].text.value
