import asyncio

from graph.nodes.ticket_rewriting_and_translating_node import TextSimilarityThreshold, TextSimilarityThresholds
from ticket_generator.ticket_generator import TicketGenerationConfig, TicketGenerator

if __name__ == '__main__':
    ticket_generation_config = TicketGenerationConfig(
        number_of_tickets=2_000,
        output_file="../data/training/dataset-v3_6_0-1k.json",
        number_translation_nodes=10,
        batch_size=100,
        mean_text_length=150,
        text_length_standard_deviation=100,
        text_similarity_thresholds=TextSimilarityThresholds([
            TextSimilarityThreshold(100, 0.8),
            TextSimilarityThreshold(30, 0.9),
            TextSimilarityThreshold(0, 1),

        ]))

    ticket_generator = TicketGenerator(ticket_generation_config)
    asyncio.run(ticket_generator.generate_dataset())
