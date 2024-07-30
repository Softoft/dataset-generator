import json

from tenacity import retry, retry_if_exception_type, stop_after_attempt

from ai.chat_assistant import AssistantId, ChatAssistantFactory
from graph.data.models import Priority, TicketExtraInformation, TicketQueue, TicketType
from graph.nodes.core.executable_node import ExecutableNode, INode
from graph.nodes.core.inject_storage_objects import inject_storage_objects
from util.key_value_storage import KeyValueStorage


class TicketExtraInformationNode(ExecutableNode):
    def __init__(self, parents: list[INode]):
        self.ticket_extra_information = None
        self.topic_generation_assistant = ChatAssistantFactory().create_assistant(AssistantId.TOPIC_GENERATION, 1.1)
        super().__init__(parents)

    def generate_topic_prompt(self, ticket_type: TicketType, ticket_queue: TicketQueue, ticket_priority: Priority):
        return (
            f"Generate {TicketExtraInformation.list_attributes_and_types()} for a ticket"
            f"with type {ticket_type.value}: '{ticket_type.description}'"
            f"and queue {ticket_queue.value}: '{ticket_queue.description}'"
            f"and priority {ticket_priority.value}: '{ticket_priority.description}'"
        )

    @retry(stop=stop_after_attempt(6), retry=retry_if_exception_type((TypeError, json.decoder.JSONDecodeError)))
    async def generate_topic(self, ticket_type: TicketType, ticket_queue: TicketQueue, ticket_priority: Priority):
        prompt = self.generate_topic_prompt(ticket_type, ticket_queue, ticket_priority)
        return TicketExtraInformation(**json.loads(await self.topic_generation_assistant.chat_assistant(prompt)))

    @inject_storage_objects(TicketType, TicketQueue, Priority)
    async def _execute_node(self, shared_storage: KeyValueStorage, ticket_type: TicketType,
                            ticket_queue: TicketQueue, ticket_priority: Priority) -> KeyValueStorage:
        ticket_extra_information = await self.generate_topic(ticket_type, ticket_queue, ticket_priority)
        shared_storage.save(ticket_extra_information)
        return shared_storage
