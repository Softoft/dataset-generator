from enum import Enum

import openai
from openai import AsyncOpenAI
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_random_exponential

from ai.chat_assistant_analysis import AssistantAnalyzer


class ChatAssistant:
    def __init__(self, assistant_name: str, assistant_id: str, temperature=1):
        self.assistant_name = assistant_name
        self.client = AsyncOpenAI()
        self.assistant_id = assistant_id
        self.temperature = temperature
        self.usage_analyzer = AssistantAnalyzer.get_instance()

    async def _create_run_with_retry(self, thread_id, assistant_id):
        run = await self.client.beta.threads.runs.create_and_poll(thread_id=thread_id,
                                                                  assistant_id=assistant_id,
                                                                  temperature=self.temperature)
        self.usage_analyzer.append_run(run, self.assistant_name)

    @retry(wait=wait_random_exponential(min=1, max=8), stop=stop_after_attempt(10),
           retry=retry_if_exception_type((openai.APITimeoutError, openai.RateLimitError, openai.APIConnectionError)))
    async def chat_assistant(self, prompt: str) -> str:
        open_ai_assistant = await self.client.beta.assistants.retrieve(self.assistant_id)
        thread = await self.client.beta.threads.create()
        await self.client.beta.threads.messages.create(thread_id=thread.id, role="user", content=prompt)
        await self._create_run_with_retry(thread.id, open_ai_assistant.id)
        messages = await self.client.beta.threads.messages.list(thread_id=thread.id)
        return messages.data[0].content[0].text.value


class AssistantId(Enum):
    EMAIL_ANSWER = "asst_OLhh0xGEY7Tu8x0dm8TOtxKu"
    EMAIL_GENERATION = "asst_015ugl1zMDzfMHCBVfZxnCW4"
    TOPIC_GENERATION = "asst_QY6nVFb9s7dGef1U4bZzh6fJ"
    REWRITING = "asst_FZTBVnl8Hyg0gXbDuMbiwn9d"
    TRANSLATION = "asst_0u4em1NJRrDdVwpM5zSqLeVx"
    TAG_GENERATION = "asst_RNCIbm4tFo7VaExVsHZVFPeK"


class ChatAssistantFactory:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChatAssistantFactory, cls).__new__(cls)
        return cls._instance

    def create_assistant(self, assistant_type: AssistantId, temperature=1):
        if not isinstance(assistant_type, AssistantId):
            raise ValueError(f"Invalid assistant type: {assistant_type}")
        return ChatAssistant(assistant_type.name.replace('_', ' ').title(), assistant_type.value, temperature)
