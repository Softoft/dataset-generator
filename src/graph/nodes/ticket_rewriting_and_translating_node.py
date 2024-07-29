import copy
import json
import logging

from tenacity import retry, retry_if_exception_type, stop_after_attempt

from ai.chat_assistant import ChatAssistantFactory
from graph.data.models import Language, Ticket
from util.key_value_storage import KeyValueStorage
from graph.nodes.core.executable_node import ExecutableNode, INode
from graph.nodes.core.inject_storage_objects import inject_storage_objects
from random_collections.random_collection import RandomCollectionBuilder
from util.text_similarity_calculator import compute_text_similarity


class InvalidTranslationException(Exception):
    pass


class TicketTranslationValidation:
    def __init__(self, ticket: Ticket, translated_ticket: Ticket):
        self.ticket = ticket
        self.translated_ticket = translated_ticket

    def _is_text_pair_valid(self, text1: str, text2: str) -> bool:
        try:
            similar_threshold = 0.75 if len(text1) > 100 else 0.85 if len(text1) > 30 else 1
            return compute_text_similarity(text1, text2) <= similar_threshold
        except AttributeError as e:
            logging.error(f"Error while comparing texts: {e}")
            return False

    def _is_translated_ticket_valid(self, ticket: Ticket, translated_ticket: Ticket):
        return (self._is_text_pair_valid(ticket.subject, translated_ticket.subject)
                and self._is_text_pair_valid(ticket.body, translated_ticket.body)
                and self._is_text_pair_valid(ticket.answer, translated_ticket.answer))

    def is_valid(self):
        return self._is_translated_ticket_valid(self.ticket, self.translated_ticket)


class TicketTranslationNode(ExecutableNode):
    def __init__(self, parents: list[INode]):
        self.ticket_email = None
        self.rewriting_assistant = ChatAssistantFactory.get_instance().create_rewriting_assistant(temperature=1.2)
        self.translation_assistant = ChatAssistantFactory.get_instance().create_translation_assistant(temperature=1.2)
        self.tag_generation_assistant = ChatAssistantFactory.get_instance().create_tag_generation_assistant()
        self.language_generator = RandomCollectionBuilder.build_from_value_weight_dict(
            { Language.DE: 2, Language.EN: 4, Language.FR: 1, Language.ES: 2, Language.PT: 1 })
        self.first_ticket = None
        super().__init__(parents)

    @inject_storage_objects(Ticket)
    async def _execute_node(self, shared_storage: KeyValueStorage, ticket: Ticket) -> KeyValueStorage:
        self.first_ticket = ticket
        translated_ticket = await self._generate_rewritten_and_translated_ticket(ticket)
        tagged_ticket = await self._generate_ticket_tags(translated_ticket)
        shared_storage.save_by_key("tickets", [tagged_ticket])
        return shared_storage

    def _generate_translation_prompt(self, ticket: Ticket, language):
        return (
            f"Translate following ticket to {language.value},"
            f"with subject '{ticket.subject}',"
            f"with body '{ticket.body}',"
            f"with answer '{ticket.answer}',"
        )

    def _generate_rewriting_prompt(self, ticket):
        return (
            f"Rewrite following ticket,"
            f"with subject '{ticket.subject}',"
            f"with body '{ticket.body}',"
            f"with answer '{ticket.answer}',"
        )

    def _generate_ticket_tags_prompt(self, ticket):
        return (
            f"Generate tags for following ticket,"
            f"with subject '{ticket.subject}',"
            f"with body '{ticket.body}',"
            f"with answer '{ticket.answer}',"
        )

    async def _generate_rewritten_and_translated_ticket(self, ticket: Ticket, repeats_left=3):
        if repeats_left == 0:
            logging.warning(
                "Could not generate valid translation; Tickets are too similar, but still returning new ticket")
            return ticket
        rewritten_ticket = await self._generate_rewritten_ticket(ticket)
        translated_ticket = await self._generate_translated_ticket(rewritten_ticket)
        if not TicketTranslationValidation(self.first_ticket, translated_ticket).is_valid():
            return await self._generate_rewritten_and_translated_ticket(translated_ticket, repeats_left - 1)
        return translated_ticket

    async def _generate_ticket_tags(self, ticket: Ticket):
        prompt = self._generate_ticket_tags_prompt(ticket)
        ticket_json_string = await self.tag_generation_assistant.chat_assistant(prompt)
        ticket_tags = json.loads(ticket_json_string)
        ticket.tags = ticket_tags["tags"]
        return ticket

    @retry(stop=stop_after_attempt(3), retry=retry_if_exception_type(json.decoder.JSONDecodeError))
    async def _generate_rewritten_ticket(self, ticket: Ticket):
        prompt = self._generate_rewriting_prompt(ticket)
        ticket_json_string = await self.rewriting_assistant.chat_assistant(prompt)
        rewritten_ticket_dict = json.loads(ticket_json_string)
        rewritten_ticket = copy.deepcopy(ticket).update(**rewritten_ticket_dict)

        return rewritten_ticket

    @retry(stop=stop_after_attempt(3), retry=retry_if_exception_type(json.decoder.JSONDecodeError))
    async def _generate_translated_ticket(self, ticket: Ticket):
        language = self.language_generator.get_random_value()
        while language == ticket.language:
            language = self.language_generator.get_random_value()
        prompt = self._generate_translation_prompt(ticket, language)
        ticket_json_string = await self.translation_assistant.chat_assistant(prompt)
        translated_ticket_dict = json.loads(ticket_json_string)
        translated_ticket = copy.deepcopy(ticket).update(**translated_ticket_dict)
        translated_ticket.language = language

        return translated_ticket
