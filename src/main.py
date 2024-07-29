import asyncio

from ticket_generator.ticket_generator import TicketGenerator

if __name__ == '__main__':
    ticket_generator = TicketGenerator(1_000, "../data/training/dataset-v3_3_0-1k.json",  10)
    asyncio.run(ticket_generator.generate_dataset())
