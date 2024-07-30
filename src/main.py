import asyncio
import logging

from injector import Injector

from dependency_provider import TicketGenerationModule
from ticket_generator.ticket_generator import TicketGenerator


def create_tickets():
    injector = Injector([TicketGenerationModule()])
    ticket_generator = injector.get(TicketGenerator)
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ],
        force=True
    )
    asyncio.run(ticket_generator.generate_dataset())


if __name__ == '__main__':
    create_tickets()
