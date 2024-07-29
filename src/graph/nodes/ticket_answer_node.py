import logging

from ai.chat_assistant import ChatAssistantFactory
from graph.data.models import Language, Priority, Ticket, TicketEmail, TicketExtraInformation, TicketQueue,\
    TicketType
from util.key_value_storage import KeyValueStorage
from graph.nodes.core.executable_node import ExecutableNode, INode
from graph.nodes.core.inject_storage_objects import inject_storage_objects


class TicketAnswerNode(ExecutableNode):
    def __init__(self, parents: list[INode]):
        self.ticket_email = None
        self.chat_assistant = ChatAssistantFactory.get_instance().create_email_answer_assistant(temperature=1.1)
        super().__init__(parents)

    @inject_storage_objects(TicketEmail, TicketExtraInformation, TicketQueue, Priority, TicketType)
    async def _execute_node(self, shared_storage: KeyValueStorage, ticket_email, ticket_extra_information, ticket_queue,
                            priority,
                            ticket_type) -> KeyValueStorage:
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
            business_type=ticket_extra_information.business_type,
            product=ticket_extra_information.product,
            version=ticket_extra_information.version,
            product_category=ticket_extra_information.product_category,
            product_sub_category=ticket_extra_information.product_sub_category,
            answer=answer_string,
            queue=ticket_queue,
            type=ticket_type,
            priority=priority,
            language=Language.EN
        )
