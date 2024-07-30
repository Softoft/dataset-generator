import asyncio
import logging
import os

from injector import Injector

from dependency_provider import TicketGenerationModule
from graph.data.models import Language
from graph.nodes.ticket_rewriting_and_translating_node import translate
from ticket_generator.ticket_generator import TicketGenerator


def translate_from_english_to_german():
    return translate("Hello, how are you?", Language.EN, Language.DE)


def create_tickets():
    injector = Injector([TicketGenerationModule()])
    ticket_generator = injector.get(TicketGenerator)
    logging.basicConfig(
        level=logging.WARNING,
        format='%(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )
    asyncio.run(ticket_generator.generate_dataset())


if __name__ == '__main__':
    os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
    create_tickets()
