import copy
import json
import logging
from dataclasses import dataclass

from tenacity import retry, retry_if_exception_type, stop_after_attempt

from ai.chat_assistant import AssistantId, ChatAssistantFactory
from graph.data.models import Language, Ticket
from graph.nodes.core.executable_node import ExecutableNode, INode
from graph.nodes.core.inject_storage_objects import inject_storage_objects
from random_collections.random_collection import RandomCollectionBuilder
from util.key_value_storage import KeyValueStorage
from util.text_manipulation import back_translate, translate
from util.text_similarity_calculator import compute_text_similarity


@dataclass
class TextSimilarityThreshold:
    text_length: int
    similarity_threshold: float


@dataclass
class TextSimilarityThresholds:
    text_lengths: list[TextSimilarityThreshold]

    def get_descending_thresholds(self):
        return sorted(self.text_lengths, key=lambda x: x.text_length, reverse=True)


def get_translated_ticket(ticket: Ticket, target_language: Language):
    assert ticket.language != target_language
    translated_ticket = copy.deepcopy(ticket)

    new_subject, new_body, new_answer = translate([ticket.subject, ticket.body, ticket.answer], ticket.language,
                                                  target_language)
    translated_ticket.update(
        language=target_language,
        subject=new_subject,
        body=new_body,
        answer=new_answer
    )
    return translated_ticket


def get_augmented_ticket(ticket: Ticket) -> Ticket:
    augmented_ticket = copy.deepcopy(ticket)
    new_subject, new_body, new_answer = back_translate([ticket.subject, ticket.body, ticket.answer], ticket.language)
    augmented_ticket.update(
        subject=new_subject,
        body=new_body,
        answer=new_answer
    )
    return augmented_ticket


class TicketSimilarityValidation:
    def __init__(self, ticket: Ticket, translated_ticket: Ticket, text_similarity_thresholds: TextSimilarityThresholds):
        self.ticket = ticket
        self.translated_ticket = translated_ticket
        self.text_similarity_thresholds = text_similarity_thresholds

    def _is_text_pair_valid(self, text1: str, text2: str) -> bool:
        try:
            similar_threshold = 1
            for threshold in self.text_similarity_thresholds.get_descending_thresholds():
                if len(text1) > threshold.text_length:
                    similar_threshold = threshold.similarity_threshold
                    break
            return compute_text_similarity(text1, text2) <= similar_threshold
        except AttributeError as e:
            logging.error(f"Error while comparing texts: {e}")
            return False

    def _is_translated_ticket_valid(self, ticket: Ticket, translated_ticket: Ticket):
        return (self._is_text_pair_valid(ticket.subject, translated_ticket.subject)
                and self._is_text_pair_valid(ticket.body, translated_ticket.body)
                and self._is_text_pair_valid(ticket.answer, translated_ticket.answer))

    def is_valid(self):
        try:
            return self._is_translated_ticket_valid(self.ticket, self.translated_ticket)
        except Exception as e:
            logging.error(f"Error while validating ticket translation: {e}")
            return False


class TicketTranslationNode(ExecutableNode):
    def __init__(self, parents: list[INode], text_similarity_thresholds: TextSimilarityThresholds):
        self.text_similarity_thresholds = text_similarity_thresholds
        self.ticket_email = None
        self.tag_generation_assistant = ChatAssistantFactory().create_assistant(AssistantId.TAG_GENERATION, 1.1)
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

    def _generate_ticket_tags_prompt(self, ticket: Ticket):
        return (f"Generate tags for the following ticket:"
                f"subject: '{ticket.subject}', "
                f"body: '{ticket.body}', "
                f"answer: '{ticket.answer}', ")

    def _generate_rewritten_and_translated_ticket(self, ticket: Ticket, repeats_left=6):
        language = self.language_generator.get_random_value(excluding=[ticket.language])
        if repeats_left == 0:
            logging.warning("Could not generate valid translation; Tickets are too similar,returning new ticket")
            return ticket
        rewritten_ticket = get_augmented_ticket(ticket)
        if not TicketSimilarityValidation(self.first_ticket, rewritten_ticket,
                                          self.text_similarity_thresholds).is_valid():
            return self._generate_rewritten_and_translated_ticket(rewritten_ticket, repeats_left - 1)
        translated_ticket = get_translated_ticket(rewritten_ticket, language)
        return translated_ticket

    @retry(stop=stop_after_attempt(3), retry=retry_if_exception_type(json.decoder.JSONDecodeError))
    async def _generate_ticket_tags(self, ticket: Ticket) -> Ticket:
        prompt = self._generate_ticket_tags_prompt(ticket)
        ticket_tags = json.loads(await self.tag_generation_assistant.chat_assistant(prompt))
        ticket.tags = ticket_tags["tags"] if "tags" in ticket_tags else []
        return ticket
