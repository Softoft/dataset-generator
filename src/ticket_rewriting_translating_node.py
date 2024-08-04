import copy
import json
import logging
from dataclasses import dataclass

from tenacity import retry, retry_if_exception_type, stop_after_attempt

from models import Language, Ticket
from synthetic_data_generator.ai_graph.key_value_store import KeyValueStore
from synthetic_data_generator.ai_graph.nodes.core.executable_node import ExecutableNode, INode
from synthetic_data_generator.ai_graph.nodes.core.inject_storage_objects import inject_storage_objects
from synthetic_data_generator.random_generators.random_collection import RandomCollectionFactory


@dataclass
class TextSimilarityThreshold:
    text_length: int
    similarity_threshold: float


@dataclass
class TextSimilarityThresholds:
    text_lengths: list[TextSimilarityThreshold]

    def get_descending_thresholds(self):
        return sorted(self.text_lengths, key=lambda x: x.text_length, reverse=True)


class TicketTranslationNode(ExecutableNode):
    def __init__(self, parents: list[INode], text_similarity_thresholds: TextSimilarityThresholds):
        self.text_similarity_thresholds = text_similarity_thresholds
        self.ticket_email = None
        self.rewriting_assistant = None
        self.translation_assistant = None
        self.tag_generation_assistant = None
        self.language_generator = RandomCollectionFactory.build_from_value_weight_dict(
            { Language.DE: 2, Language.EN: 4, Language.FR: 1, Language.ES: 2, Language.PT: 1 })
        self.first_ticket = None
        super().__init__(parents)

    @inject_storage_objects(Ticket)
    async def _execute_node(self, shared_storage: KeyValueStore, ticket: Ticket) -> KeyValueStore:
        self.first_ticket = ticket
        translated_ticket = await self._generate_rewritten_and_translated_ticket(ticket)
        tagged_ticket = await self._generate_ticket_tags(translated_ticket)
        shared_storage.save_by_key("tickets", [tagged_ticket])
        return shared_storage

    def _generate_ticket_text_prompt(self, ticket: Ticket):
        return (
            f"Ticket:"
            f"subject: '{ticket.subject}', "
            f"body: '{ticket.body}', "
            f"answer: '{ticket.answer}', "
        )

    def _generate_translation_prompt(self, ticket: Ticket, language):
        return f"Translate following ticket_a to {language.value}, {self._generate_ticket_text_prompt(ticket)}"

    def _generate_rewriting_prompt(self, ticket):
        return f"Rewrite following ticket_a, {self._generate_ticket_text_prompt(ticket)}"

    def _generate_ticket_tags_prompt(self, ticket):
        return f"Generate tags for the following ticket_a, {self._generate_ticket_text_prompt(ticket)}"

    async def _generate_rewritten_and_translated_ticket(self, ticket: Ticket, repeats_left=2):
        if repeats_left == 0:
            logging.warning(
                "Could not generate valid translation; Tickets are too similar, but still returning new ticket_a")
            return ticket
        rewritten_ticket = await self._generate_rewritten_ticket(ticket)
        back_translated_ticket = await self._generate_translated_ticket(rewritten_ticket, self.first_ticket.language)
        random_language = self.language_generator.get_random_value()
        translated_ticket = await self._generate_translated_ticket(ticket, random_language)
        return translated_ticket

    @retry(stop=stop_after_attempt(3), retry=retry_if_exception_type(json.decoder.JSONDecodeError))
    async def _generate_ticket_tags(self, ticket: Ticket):
        prompt = self._generate_ticket_tags_prompt(ticket)
        ticket_tags = json.loads(await self.tag_generation_assistant.chat_assistant(prompt))
        ticket.tags = ticket_tags["tags"] if "tags" in ticket_tags else []
        return ticket

    @retry(stop=stop_after_attempt(3), retry=retry_if_exception_type(json.decoder.JSONDecodeError))
    async def _generate_rewritten_ticket(self, ticket: Ticket):
        prompt = self._generate_rewriting_prompt(ticket)
        rewritten_ticket_dict = json.loads(await self.rewriting_assistant.chat_assistant(prompt))
        rewritten_ticket = copy.deepcopy(ticket).update(subject=rewritten_ticket_dict['subject'],
                                                        body=rewritten_ticket_dict['body'],
                                                        answer=rewritten_ticket_dict['answer'])
        return rewritten_ticket

    @retry(stop=stop_after_attempt(3), retry=retry_if_exception_type(json.decoder.JSONDecodeError))
    async def _generate_translated_ticket(self, ticket: Ticket, target_language: Language):
        if ticket.language == target_language:
            return ticket
        prompt = self._generate_translation_prompt(ticket, target_language)
        translated_ticket_dict = json.loads(await self.translation_assistant.chat_assistant(prompt))
        translated_ticket = copy.deepcopy(ticket).update(subject=translated_ticket_dict['subject'],
                                                         body=translated_ticket_dict['body'],
                                                         answer=translated_ticket_dict['answer'])
        translated_ticket.language = target_language

        return translated_ticket
