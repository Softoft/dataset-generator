import json
import logging
from dataclasses import dataclass

import openai
from openai import AsyncOpenAI
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_random_exponential

from synthetic_data_generator.ai_graph.ai.chat_assistant_analysis import cost_analyzer
from synthetic_data_generator.ai_graph.ai.chat_assistant_config import AssistantModel


@cost_analyzer()
@dataclass
class ChatAssistant:
    assistant_name: str
    assistant_id: str
    model: AssistantModel
    temperature: float
    client: AsyncOpenAI

    async def create_run(self, thread_id, assistant_id):
        logging.info(f"Creating run for thread {thread_id} and assistant {assistant_id}")
        return await self.client.beta.threads.runs.create_and_poll(thread_id=thread_id,
                                                                   assistant_id=assistant_id,
                                                                   temperature=self.temperature)

    @retry(wait=wait_random_exponential(min=4, max=128), stop=stop_after_attempt(20),
           retry=retry_if_exception_type((openai.APITimeoutError, openai.RateLimitError, openai.APIConnectionError)))
    async def get_response(self, prompt: str) -> str:
        open_ai_assistant = await self.client.beta.assistants.retrieve(self.assistant_id)
        thread = await self.client.beta.threads.create()
        await self.client.beta.threads.messages.create(thread_id=thread.id, role="user", content=prompt)
        await self.create_run(thread.id, open_ai_assistant.id)
        messages = await self.client.beta.threads.messages.list(thread_id=thread.id)
        message = messages.data[0].content[0].text.value
        logging.info(f"Got response: \"{message}\"")
        return message

    async def get_dict_response(self, prompt: str) -> dict:
        return json.loads(await self.get_response(prompt))
