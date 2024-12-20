import json

from tenacity import retry, retry_if_exception_type, stop_after_attempt

from models import Priority, TicketExtraInformation, TicketQueue, TicketType
from synthetic_data_generator.ai_graph.key_value_store import KeyValueStore, inject_storage_objects
from synthetic_data_generator.ai_graph.nodes.executable_node import ExecutableNode, INode


class TicketExtraInformationNode(ExecutableNode):
    def __init__(self, parents: list[INode] = None):
        self.topic_generation_assistant = None
        super().__init__(parents or [])

    def generate_topic_prompt(self, ticket_type: TicketType, ticket_queue: TicketQueue, ticket_priority: Priority):
        return (
            f"Generate {TicketExtraInformation.list_attributes_and_types()} for a ticket:"
            f"type: '{ticket_type.value}', "
            f"queue: '{ticket_queue.value}', "
            f"priority: '{ticket_priority.value}'"
        )

    @retry(stop=stop_after_attempt(6),
           retry=retry_if_exception_type((TypeError, json.decoder.JSONDecodeError, AssertionError)))
    async def generate_topic(self, ticket_type: TicketType, ticket_queue: TicketQueue, ticket_priority: Priority):
        prompt = self.generate_topic_prompt(ticket_type, ticket_queue, ticket_priority)
        return TicketExtraInformation(**json.loads(await self.topic_generation_assistant.get_response(prompt)))

    @inject_storage_objects(TicketType, TicketQueue, Priority)
    async def _execute_node(self, shared_storage: KeyValueStore, ticket_type: TicketType,
                            ticket_queue: TicketQueue, ticket_priority: Priority) -> KeyValueStore:
        ticket_extra_information = await self.generate_topic(ticket_type, ticket_queue, ticket_priority)
        shared_storage.save(ticket_extra_information)
        return shared_storage
