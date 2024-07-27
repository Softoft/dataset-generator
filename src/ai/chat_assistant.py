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
    def __init__(self, assistant_id, tool_choice: AssistantToolChoiceOptionParam = "auto", temperature=1, model="gpt-4o"):
        self.client = AsyncOpenAI()
        self.assistant_id = assistant_id
        self.tool_choice: AssistantToolChoiceOptionParam = tool_choice
        self.temperature = temperature
        self.model: str = model
        self.assistant_analysis = AssistantAnalysis()

    @retry(wait=wait_random_exponential(min=1, max=4), stop=stop_after_attempt(2))
    async def _create_run_with_retry(self, thread_id, assistant_id) -> Run:
        run = await self.client.beta.threads.runs.create_and_poll(thread_id=thread_id,
                                                                  assistant_id=assistant_id,
                                                                  temperature=self.temperature,
                                                                  tool_choice=self.tool_choice,
                                                                  model=self.model)
        self.assistant_analysis.append_run(run)
        return run

    @retry(wait=wait_random_exponential(min=1, max=4), stop=stop_after_attempt(2))
    async def chat_assistant(self, prompt: str) -> str:
        open_ai_assistant = await self.client.beta.assistants.retrieve(self.assistant_id)
        thread = await self.client.beta.threads.create()
        await self.client.beta.threads.messages.create(thread_id=thread.id, role="user", content=prompt)
        run = await self._create_run_with_retry(thread.id, open_ai_assistant.id)
        self.assistant_analysis.append_run(run)
        messages = await self.client.beta.threads.messages.list(thread_id=thread.id)
        return messages.data[0].content[0].text.value
