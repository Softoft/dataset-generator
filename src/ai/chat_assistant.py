from dataclasses import dataclass
from enum import Enum

import openai
from openai import AsyncOpenAI
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_random_exponential

from ai.chat_assistant_analysis import AssistantAnalyzer


class AssistantModel(Enum):
    GPT4_O = "gpt4-o"
    GPT4_o_MINI = "gpt4-o-mini"


@dataclass
class ChatAssistantConfig:
    assistant_name: str
    assistant_id: str
    model: AssistantModel
    temperature: float


@dataclass
class ChatAssistant:
    client: AsyncOpenAI
    usage_analyzer: AssistantAnalyzer
    chat_assistant_config: ChatAssistantConfig

    async def _create_run_with_retry(self, thread_id, assistant_id):
        run = await self.client.beta.threads.runs.create_and_poll(thread_id=thread_id,
                                                                  assistant_id=assistant_id,
                                                                  temperature=self.temperature)
        self.usage_analyzer.append_run(run, self.assistant_name)

    @retry(wait=wait_random_exponential(min=4, max=128), stop=stop_after_attempt(20),
           retry=retry_if_exception_type((openai.APITimeoutError, openai.RateLimitError, openai.APIConnectionError)))
    async def chat_assistant(self, prompt: str) -> str:
        open_ai_assistant = await self.client.beta.assistants.retrieve(self.assistant_id)
        thread = await self.client.beta.threads.create()
        await self.client.beta.threads.messages.create(thread_id=thread.id, role="user", content=prompt)
        await self._create_run_with_retry(thread.id, open_ai_assistant.id)
        messages = await self.client.beta.threads.messages.list(thread_id=thread.id)
        return messages.data[0].content[0].text.value
