from dataclasses import dataclass

from graph.nodes.ticket_rewriting_translating_node import TextSimilarityThresholds


@dataclass
class Config:
    number_of_tickets: int
    output_file: str
    number_translation_nodes: int
    text_length_mean: int
    text_length_standard_deviation: int
    batch_size: int
    text_similarity_thresholds: TextSimilarityThresholds
