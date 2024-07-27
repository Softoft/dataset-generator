import asyncio
import json

from ai.chat_assistant import ChatAssistant
from graph.data.ticket_extra_information import TicketExtraInformation
from graph.data.ticket_queue import TicketQueue
from graph.data.ticket_type import TicketType
from graph.nodes.core.executable_node import ExecutableNode, INode
from graph.nodes.core.inject_storage_objects import inject_storage_objects
from graph.nodes.core.save_execute_state import save_execute_state
from storage.key_value_storage import KeyValueStorage

TOPIC_GENERATION_ASSISTANT = "asst_QY6nVFb9s7dGef1U4bZzh6fJ"


@save_execute_state(lambda self: self.ticket_extra_information)
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

    def generate_topic(self, ticket_type: TicketType, ticket_queue: TicketQueue):
        prompt = self.generate_topic_prompt(ticket_type, ticket_queue)
        email_json_string = asyncio.run(self.chat_assistant.chat_assistant(prompt))
        email_dict = json.loads(email_json_string)
        return TicketExtraInformation(**email_dict)

    @inject_storage_objects(TicketType, TicketQueue)
    def _execute_node(self, shared_storage: KeyValueStorage, ticket_type: TicketType, ticket_queue: TicketQueue) -> KeyValueStorage:
        ticket_extra_information = self.generate_topic(ticket_type, ticket_queue)
        shared_storage.save(ticket_extra_information)
        return shared_storage
