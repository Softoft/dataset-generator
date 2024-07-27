import asyncio
import json

from ai.chat_assistant import ChatAssistant
from graph.data.priority import Priority
from graph.data.ticket_email import TicketEmail
from graph.data.ticket_extra_information import TicketExtraInformation
from graph.data.ticket_queue import TicketQueue
from graph.data.ticket_text_length import TicketTextLength
from graph.data.ticket_type import TicketType
from graph.nodes.core.executable_node import ExecutableNode, INode
from graph.nodes.core.inject_storage_objects import inject_storage_objects
from graph.nodes.core.save_execute_state import save_execute_state
from storage.key_value_storage import KeyValueStorage

EMAIL_GENERATION_ASSISTANT_ID = "asst_015ugl1zMDzfMHCBVfZxnCW4"


@save_execute_state(lambda self: self.ticket_email)
class TicketEmailNode(ExecutableNode):
    def __init__(self, parents: list[INode]):
        self.ticket_email = None
        self.chat_assistant = ChatAssistant(EMAIL_GENERATION_ASSISTANT_ID)
        super().__init__(parents)

    @inject_storage_objects(TicketType, TicketQueue, Priority, TicketTextLength, TicketExtraInformation)
    def _execute_node(self, shared_storage: KeyValueStorage, ticket_type: TicketType, ticket_queue: TicketQueue,
                      ticket_priority: Priority, ticket_text_length: TicketTextLength,
                      ticket_extra_information: TicketExtraInformation) -> KeyValueStorage:
        ticket_email = self._generate_email(ticket_type, ticket_queue, ticket_priority, ticket_text_length,
                                            ticket_extra_information)
        shared_storage.save(ticket_email)
        return shared_storage

    def _generate_email_prompt(self, ticket_type: TicketType, ticket_queue: TicketQueue, priority: Priority,
                               ticket_text_length: TicketTextLength, ticket_extra_information: TicketExtraInformation):
        return (
            f"Generate email text and subject."
            f"About the topic {ticket_extra_information.topic} and the product: {ticket_extra_information.product},"
            f"For a ticket, with type {ticket_type.value}: {ticket_type.description},"
            f"for the queue {ticket_queue.value}: {ticket_queue.description},"
            f"for the priority {priority.value}: {priority.description},"
            f"The text needs to have between  {ticket_text_length.lower_bound} and {ticket_text_length.upper_bound} characters")

    def _generate_email(self, ticket_type: TicketType, ticket_queue: TicketQueue, priority: Priority,
                        ticket_text_length: TicketTextLength, ticket_extra_information: TicketExtraInformation):
        prompt = self._generate_email_prompt(ticket_type, ticket_queue, priority, ticket_text_length,
                                             ticket_extra_information)
        email_json_string = asyncio.run(self.chat_assistant.chat_assistant(prompt))
        email_dict = json.loads(email_json_string)
        return TicketEmail(**email_dict)
