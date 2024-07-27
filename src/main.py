import asyncio

from ticket_generator.ticket_generator import TicketGenerator

if __name__ == '__main__':
    ticket_generator = TicketGenerator(20, "../data/training/gpt-4-multi-lang-big-1k-randomized.json",
                                       10)

    asyncio.run(ticket_generator.generate_dataset())
