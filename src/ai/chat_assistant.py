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

    @retry(wait=wait_random_exponential(min=1, max=120), stop=stop_after_attempt(10),
           retry=retry_if_exception_type((openai.APITimeoutError, openai.RateLimitError, openai.APIConnectionError)))
    async def chat_assistant(self, prompt: str) -> str:
        open_ai_assistant = await self.client.beta.assistants.retrieve(self.assistant_id)
        thread = await self.client.beta.threads.create()
        await self.client.beta.threads.messages.create(thread_id=thread.id, role="user", content=prompt)
        await self._create_run_with_retry(thread.id, open_ai_assistant.id)
        messages = await self.client.beta.threads.messages.list(thread_id=thread.id)
        return messages.data[0].content[0].text.value


class ChatAssistantFactory:
    _instance = None
    EMAIL_ANSWER_ASSISTANT_ID = "asst_OLhh0xGEY7Tu8x0dm8TOtxKu"
    EMAIL_GENERATION_ASSISTANT_ID = "asst_015ugl1zMDzfMHCBVfZxnCW4"
    TOPIC_GENERATION_ASSISTANT = "asst_QY6nVFb9s7dGef1U4bZzh6fJ"
    TICKET_REWRITING_ASSISTANT_ID = "asst_FZTBVnl8Hyg0gXbDuMbiwn9d"
    Ticket_TRANSLATION_ASSISTANT_ID = "asst_0u4em1NJRrDdVwpM5zSqLeVx"
    TAG_GENERATION_ASSISTANT_ID = "asst_RNCIbm4tFo7VaExVsHZVFPeK"

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = ChatAssistantFactory()
        return cls._instance

    def create_email_answer_assistant(self, temperature=1):
        return ChatAssistant("Email Answer Assistant", self.EMAIL_ANSWER_ASSISTANT_ID, temperature=temperature)

    def create_email_generation_assistant(self, temperature=1):
        return ChatAssistant("Email Generation Assistant", self.EMAIL_GENERATION_ASSISTANT_ID, temperature=temperature)

    def create_topic_generation_assistant(self, temperature=1):
        return ChatAssistant("Topic Generation Assistant", self.TOPIC_GENERATION_ASSISTANT, temperature=temperature)

    def create_rewriting_assistant(self, temperature=1):
        return ChatAssistant("Rewriting Assistant", self.TICKET_REWRITING_ASSISTANT_ID, temperature=temperature)

    def create_translation_assistant(self, temperature=1):
        return ChatAssistant("Translation Assistant", self.Ticket_TRANSLATION_ASSISTANT_ID, temperature=temperature)

    def create_tag_generation_assistant(self, temperature=1):
        return ChatAssistant("Tag Generation Assistant", self.TAG_GENERATION_ASSISTANT_ID, temperature=temperature)
