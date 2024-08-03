from dataclasses import dataclass


@dataclass
class Config:
    number_of_tickets: int
    output_file: str
    number_translation_nodes: int
    text_length_mean: int
    text_length_standard_deviation: int
    batch_size: int
    max_text_similarity: float
    min_content_similarity: float
