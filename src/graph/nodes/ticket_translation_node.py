import asyncio
import json
import logging

from ai.chat_assistant import ChatAssistant
from graph.data.models import Language, Ticket, TranslatedTicket, TicketEmail
from graph.key_value_storage import KeyValueStorage
from graph.nodes.core.executable_node import ExecutableNode, INode
from graph.nodes.core.inject_storage_objects import inject_storage_objects

Ticket_TRANSLATION_ASSISTANT_ID = "asst_0u4em1NJRrDdVwpM5zSqLeVx"


class TicketTranslationNode(ExecutableNode):
    def __init__(self, parents: list[INode]):
        self.ticket_email = None
        self.chat_assistant = ChatAssistant(Ticket_TRANSLATION_ASSISTANT_ID)
        super().__init__(parents)

    @inject_storage_objects(Ticket, Language)
    async def _execute_node(self, shared_storage: KeyValueStorage, ticket, language) -> KeyValueStorage:
        translated_ticket = await self._generate_translated_ticket(ticket, language)
        shared_storage.save(translated_ticket)
        return shared_storage

    def _generate_translation_prompt(self, ticket, language):
        return (
            f"Translate following ticket to {language.value},"
            f"with subject '{ticket.subject}',"
            f"with body '{ticket.body}',"
            f"with answer '{ticket.answer}',"
        )

    async def _generate_translated_ticket(self, ticket: Ticket, language: Language):
        prompt = self._generate_translation_prompt(ticket, language)
        logging.warning(f"PROMPT: {prompt}")
        ticket_json_string = await self.chat_assistant.chat_assistant(prompt)
        translated_ticket_dict = json.loads(ticket_json_string)
        return TranslatedTicket(
            subject=translated_ticket_dict["subject"],
            body=translated_ticket_dict["body"],
            answer=translated_ticket_dict["answer"],
            queue=ticket.queue,
            type=ticket.type,
            priority=ticket.priority,
            language=language
        )
