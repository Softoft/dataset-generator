import asyncio
import json

from tenacity import retry, retry_if_exception_type, stop_after_attempt

from ai.chat_assistant import ChatAssistant
from graph.data.models import TicketExtraInformation, TicketQueue, TicketType
from graph.nodes.core.executable_node import ExecutableNode, INode
from graph.nodes.core.inject_storage_objects import inject_storage_objects
from graph.key_value_storage import KeyValueStorage

TOPIC_GENERATION_ASSISTANT = "asst_QY6nVFb9s7dGef1U4bZzh6fJ"


class TicketExtraInformationNode(ExecutableNode):
    def __init__(self, parents: list[INode]):
        self.ticket_extra_information = None
        self.chat_assistant = ChatAssistant(TOPIC_GENERATION_ASSISTANT, temperature=1.3)
        super().__init__(parents)

    def generate_topic_prompt(self, ticket_type: TicketType, ticket_queue: TicketQueue):
        return (
            f"Generate topic, product_category and product for a ticket,"
            f"with type {ticket_type.value}: {ticket_type.description};"
            f"and queue {ticket_queue.value}: {ticket_queue.description}"
        )

    @retry(stop=stop_after_attempt(3), retry=retry_if_exception_type(TypeError))
    async def generate_topic(self, ticket_type: TicketType, ticket_queue: TicketQueue):
        prompt = self.generate_topic_prompt(ticket_type, ticket_queue)
        email_json_string = await self.chat_assistant.chat_assistant(prompt)
        email_dict = json.loads(email_json_string)
        return TicketExtraInformation(**email_dict)

    @inject_storage_objects(TicketType, TicketQueue)
    async def _execute_node(self, shared_storage: KeyValueStorage, ticket_type: TicketType, ticket_queue: TicketQueue) -> KeyValueStorage:
        ticket_extra_information = await self.generate_topic(ticket_type, ticket_queue)
        shared_storage.save(ticket_extra_information)
        return shared_storage
