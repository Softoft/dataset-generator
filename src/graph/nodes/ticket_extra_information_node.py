import json

from tenacity import retry, retry_if_exception_type, stop_after_attempt

from ai.chat_assistant import ChatAssistantFactory
from graph.data.models import Priority, TicketExtraInformation, TicketQueue, TicketType
from util.key_value_storage import KeyValueStorage
from graph.nodes.core.executable_node import ExecutableNode, INode
from graph.nodes.core.inject_storage_objects import inject_storage_objects


class TicketExtraInformationNode(ExecutableNode):
    def __init__(self, parents: list[INode]):
        self.ticket_extra_information = None
        self.topic_generation_assistant = ChatAssistantFactory.get_instance().create_topic_generation_assistant(temperature=1.1)
        super().__init__(parents)

    def generate_topic_prompt(self, ticket_type: TicketType, ticket_queue: TicketQueue, ticket_priority: Priority):
        return (
            f"Generate ticket_categories, business_type, product_category, product_sub_category, product, version, extra_info for a ticket"
            f"with type {ticket_type.value}: {ticket_type.description};"
            f"and queue {ticket_queue.value}: {ticket_queue.description};"
            f"and priority {ticket_priority.value}: {ticket_priority.description}"
        )

    @retry(stop=stop_after_attempt(6), retry=retry_if_exception_type((TypeError, json.decoder.JSONDecodeError)))
    async def generate_topic(self, ticket_type: TicketType, ticket_queue: TicketQueue, ticket_priority: Priority):
        prompt = self.generate_topic_prompt(ticket_type, ticket_queue, ticket_priority)
        ticket_extra_info_str = await self.topic_generation_assistant.chat_assistant(prompt)
        ticket_extra_info_email_dict = json.loads(ticket_extra_info_str)
        return TicketExtraInformation(**ticket_extra_info_email_dict)

    @inject_storage_objects(TicketType, TicketQueue, Priority)
    async def _execute_node(self, shared_storage: KeyValueStorage, ticket_type: TicketType,
                            ticket_queue: TicketQueue, ticket_priority: Priority) -> KeyValueStorage:
        ticket_extra_information = await self.generate_topic(ticket_type, ticket_queue, ticket_priority)
        shared_storage.save(ticket_extra_information)
        return shared_storage
