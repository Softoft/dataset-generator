import asyncio

from ticket_generator.ticket_generator import TicketGenerator

if __name__ == '__main__':
    ticket_generator = TicketGenerator(2, "../data/training/gpt-4-multi-lang-big-1k-randomized.json",
                                       1)

    asyncio.run(ticket_generator.generate_dataset())
