import asyncio
import json
import logging

from ai.chat_assistant import ChatAssistant
from graph.data.models import Priority, Ticket, TranslatedTicket, TicketEmail, TicketExtraInformation, TicketQueue,\
    TicketTextLength,\
    TicketType
from graph.nodes.core.executable_node import ExecutableNode, INode
from graph.nodes.core.inject_storage_objects import inject_storage_objects
from graph.key_value_storage import KeyValueStorage

EMAIL_ANSER_ASSISTANT_ID = "asst_OLhh0xGEY7Tu8x0dm8TOtxKu"


class TicketAnswerNode(ExecutableNode):
    def __init__(self, parents: list[INode]):
        self.ticket_email = None
        self.chat_assistant = ChatAssistant(EMAIL_ANSER_ASSISTANT_ID)
        super().__init__(parents)

    @inject_storage_objects(TicketEmail, TicketQueue, Priority, TicketType)
    async def _execute_node(self, shared_storage: KeyValueStorage, ticket, ticket_queue, priority, ticket_type) -> KeyValueStorage:
        ticket = await self._generate_ticket(ticket, ticket_queue, priority, ticket_type)
        shared_storage.save(ticket)
        return shared_storage

    def _generate_email_prompt(self, ticket_email: TicketEmail):
        return (
            f"Answer to the following email: '{ticket_email.subject}', with the following body: '{ticket_email.body}',")

    async def _generate_ticket(self, ticket_email: TicketEmail, ticket_queue: TicketQueue, priority: Priority, ticket_type: TicketType):
        prompt = self._generate_email_prompt(ticket_email)
        logging.warning(f"PROMPT: {prompt}")
        answer_string = await self.chat_assistant.chat_assistant(prompt)
        return Ticket(
            subject=ticket_email.subject,
            body=ticket_email.body,
            answer=answer_string,
            queue=ticket_queue,
            type=ticket_type,
            priority=priority
        )
