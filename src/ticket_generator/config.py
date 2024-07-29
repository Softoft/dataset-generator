from dataclasses import dataclass

from graph.nodes.ticket_rewriting_and_translating_node import TextSimilarityThresholds


@dataclass
class TicketGenerationConfig:
    number_of_tickets: int
    output_file: str
    number_translation_nodes: int
    mean_text_length: int
    text_length_standard_deviation: int
    batch_size: int
    text_similarity_thresholds: TextSimilarityThresholds