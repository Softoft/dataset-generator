import asyncio

from ticket_generator.ticket_generator import TicketGenerator

if __name__ == '__main__':
    ticket_generator = TicketGenerator(400, "../data/training/dataset-v3_1_0-sample.json",  10)
    asyncio.run(ticket_generator.generate_dataset())
