import openai
from openai import AsyncOpenAI
from openai.types.beta import AssistantToolChoiceOptionParam
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_random_exponential

from ai.chat_assistant_analysis import AssistantAnalyzer


class ChatAssistant:
    def __init__(self, assistant_id, tool_choice: AssistantToolChoiceOptionParam = "auto", temperature=1,
                 model="gpt-4o"):
        self.client = AsyncOpenAI()
        self.assistant_id = assistant_id
        self.tool_choice: AssistantToolChoiceOptionParam = tool_choice
        self.temperature = temperature
        self.model: str = model
        self.usage_analyzer = AssistantAnalyzer()

    async def _create_run_with_retry(self, thread_id, assistant_id):
        run = await self.client.beta.threads.runs.create_and_poll(thread_id=thread_id,
                                                                  assistant_id=assistant_id,
                                                                  temperature=self.temperature,
                                                                  tool_choice=self.tool_choice,
                                                                  model=self.model)
        self.usage_analyzer.append_run(run)

    @retry(wait=wait_random_exponential(min=1, max=120), stop=stop_after_attempt(10),
           retry=retry_if_exception_type((openai.APITimeoutError, openai.RateLimitError)))
    async def chat_assistant(self, prompt: str) -> str:
        open_ai_assistant = await self.client.beta.assistants.retrieve(self.assistant_id)
        thread = await self.client.beta.threads.create()
        await self.client.beta.threads.messages.create(thread_id=thread.id, role="user", content=prompt)
        await self._create_run_with_retry(thread.id, open_ai_assistant.id)
        messages = await self.client.beta.threads.messages.list(thread_id=thread.id)
        return messages.data[0].content[0].text.value
