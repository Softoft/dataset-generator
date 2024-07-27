import asyncio
import json
import logging

from ai.chat_assistant import ChatAssistant
from graph.data.models import Priority, TicketEmail, TicketExtraInformation, TicketQueue, TicketTextLength, TicketType
from graph.key_value_storage import KeyValueStorage
from graph.nodes.core.executable_node import ExecutableNode, INode
from graph.nodes.core.inject_storage_objects import inject_storage_objects

EMAIL_GENERATION_ASSISTANT_ID = "asst_015ugl1zMDzfMHCBVfZxnCW4"


class TicketEmailNode(ExecutableNode):
    def __init__(self, parents: list[INode]):
        self.ticket_email = None
        self.chat_assistant = ChatAssistant(EMAIL_GENERATION_ASSISTANT_ID)
        super().__init__(parents)

    @inject_storage_objects(TicketType, TicketQueue, Priority, TicketTextLength, TicketExtraInformation)
    async def _execute_node(self, shared_storage: KeyValueStorage, ticket_type, ticket_queue, ticket_priority,
                            ticket_text_length,
                            ticket_extra_information) -> KeyValueStorage:
        ticket_email = await self._generate_email(ticket_type, ticket_queue, ticket_priority, ticket_text_length,
                                            ticket_extra_information)
        shared_storage.save(ticket_email)
        return shared_storage

    def _generate_email_prompt(self, ticket_type, ticket_queue, priority, ticket_text_length, ticket_extra_information):
        return (
            f"Generate email text and subject."
            f"About the topic '{ticket_extra_information.topic}' and the product: '{ticket_extra_information.product}',"
            f"For a ticket, with type '{ticket_type.value}': '{ticket_type.description}',"
            f"for the queue '{ticket_queue.value}': '{ticket_queue.description}',"
            f"for the priority '{priority.value}': '{priority.description}',"
            f"The text needs to have between '{ticket_text_length.lower_bound}' and '{ticket_text_length.upper_bound}' characters")

    async def _generate_email(self, ticket_type: TicketType, ticket_queue: TicketQueue, priority: Priority,
                        ticket_text_length: TicketTextLength, ticket_extra_information: TicketExtraInformation):
        prompt = self._generate_email_prompt(ticket_type, ticket_queue, priority, ticket_text_length,
                                             ticket_extra_information)
        logging.warning(f"PROMPT: {prompt}")
        email_json_string = await self.chat_assistant.chat_assistant(prompt)
        email_dict = json.loads(email_json_string)
        return TicketEmail(**email_dict)
