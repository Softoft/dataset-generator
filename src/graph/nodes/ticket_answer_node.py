import logging

from ai.chat_assistant import AssistantId, ChatAssistantFactory
from graph.data.models import Language, Priority, Ticket, TicketEmail, TicketExtraInformation, TicketQueue,\
    TicketType
from graph.nodes.core.executable_node import ExecutableNode, INode
from graph.nodes.core.inject_storage_objects import inject_storage_objects
from util.key_value_storage import KeyValueStore


class TicketAnswerNode(ExecutableNode):
    def __init__(self, parents: list[INode]):
        self.ticket_email = None
        self.chat_assistant = ChatAssistantFactory().create_assistant(AssistantId.EMAIL_ANSWER, temperature=1.1)
        super().__init__(parents)

    @inject_storage_objects(TicketEmail, TicketExtraInformation, TicketQueue, Priority, TicketType)
    async def _execute_node(self, shared_storage: KeyValueStore, ticket_email, ticket_extra_information, ticket_queue,
                            priority,
                            ticket_type) -> KeyValueStore:
        logging.info(f"TicketAnswerNode: Execute!")
        ticket = await self._generate_ticket(ticket_email, ticket_extra_information, ticket_queue, priority,
                                             ticket_type)
        shared_storage.save(ticket)
        return shared_storage

    def _generate_email_prompt(self, ticket_email: TicketEmail):
        max_answer_length = max(100, len(ticket_email.body))
        return (
            f"Answer to the following email: '{ticket_email.subject}', body: '{ticket_email.body}', Answer short, with a maximum of {max_answer_length} characters.")

    async def _generate_ticket(self, ticket_email: TicketEmail, ticket_extra_information: TicketExtraInformation,
                               ticket_queue: TicketQueue, priority: Priority, ticket_type: TicketType):
        prompt = self._generate_email_prompt(ticket_email)
        logging.info(f"PROMPT: {prompt}")
        answer_string = await self.chat_assistant.chat_assistant(prompt)
        return Ticket(
            subject=ticket_email.subject,
            body=ticket_email.body,
            ticket_extra_information=ticket_extra_information,
            answer=answer_string,
            queue=ticket_queue,
            type=ticket_type,
            priority=priority,
            language=Language.EN
        )
