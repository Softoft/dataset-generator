import asyncio

import pytest

from graph.data.models import Language, Priority, Ticket, TicketQueue, TicketType
from graph.nodes.ticket_rewriting_and_translating_node import TicketTranslationValidation
from util.text_similarity_calculator import compute_text_similarity


def test_ticket_translation_validation():
    ticket = Ticket(
        subject="Dell UltraSharp 27 - Loud Noise Issue when Powered On",
        body="I am experiencing an issue with my Dell UltraSharp 27 monitor. Each time I power it on, it makes a loud, unsettling noise. I have tried different power outlets and even reset the monitor to its default settings but the problem persists.",
        answer="I am sorry to hear that you are experiencing issues with your Dell UltraSharp 27 monitor. To better assist you, could you please provide me with the serial number of the monitor?",
        queue=TicketQueue.IT_SUPPORT,
        type=TicketType.PROBLEM,
        priority=Priority.LOW,
        language=Language.EN
    )

    translated_ticket = Ticket(
        subject="Windows XP problem",
        body="Windows not working",
        answer="I am sorry to hear that you are experiencing issues ",
        queue=TicketQueue.IT_SUPPORT,
        type=TicketType.PROBLEM,
        priority=Priority.LOW,
        language=Language.EN
    )

    assert TicketTranslationValidation(ticket, translated_ticket).is_valid()


@pytest.mark.expensive
@pytest.mark.asyncio
async def test_creating_ticket_works(create_ticket_translation_node):
    ticket_translation_node = create_ticket_translation_node()
    shared_storage = await ticket_translation_node.execute()

    ticket = shared_storage.get_by_key("tickets")[0]
    assert ticket is not None
    print(ticket)


@pytest.mark.asyncio
async def test_ticket_translations_are_unique(execute_ticket_translation_node):
    async def translate_ticket(ticket, execute_translation):
        shared_storage = await execute_translation(ticket)
        return shared_storage.get_by_key("tickets")[0]

    ticket = Ticket(
        subject="Dell UltraSharp 27 - Loud Noise Issue when Powered On",
        body="I am experiencing an issue with my Dell UltraSharp 27 monitor. Each time I power it on, it makes a loud, unsettling noise. I have tried different power outlets and even reset the monitor to its default settings but the problem persists.",
        answer="I am sorry to hear that you are experiencing issues with your Dell UltraSharp 27 monitor. To better assist you, could you please provide me with the serial number of the monitor?",
        queue=TicketQueue.IT_SUPPORT,
        type=TicketType.PROBLEM,
        priority=Priority.LOW,
    )

    translation_tasks = [
        translate_ticket(ticket, execute_ticket_translation_node) for _ in range(15)
    ]

    translated_tickets = await asyncio.gather(*translation_tasks)

    translations_by_language = { }
    for translated_ticket in translated_tickets:
        translations_by_language.setdefault(translated_ticket.language, []).append(translated_ticket)

    for language, translations in translations_by_language.items():
        check_translation_similarity(translations)


def check_translation_similarity(translations):
    for i, translation1 in enumerate(translations):
        for j, translation2 in enumerate(translations):
            if i >= j:
                continue

            check_similarity_for_pair(translation1.subject, translation2.subject)
            check_similarity_for_pair(translation1.body, translation2.body)
            check_similarity_for_pair(translation1.answer, translation2.answer)


def check_similarity_for_pair(text1: str, text2: str):
    similarity = compute_text_similarity(text1, text2)
    max_similarity = get_max_similarity_threshold(min(len(text1), len(text2)))
    similarity_assertion(text1, text2, similarity, max_similarity)


def similarity_assertion(text1, text2, similarity, max_similarity):
    assert similarity <= max_similarity, f"Texts are too similar: {text1} vs {text2}, similarity: {similarity}, max allowed: {max_similarity}"


def get_max_similarity_threshold(text_length):
    if text_length <= 30:
        return 1.0
    else:
        return 0.95
