from dataclasses import dataclass

from synthetic_data_generator.ai_graph.ai.chat_assistant import ChatAssistant
from synthetic_data_generator.random_generators.number_interval_generator import NumberInterval, NumberIntervalGenerator


@dataclass
class BasicConfig:
    number_of_tickets: int
    output_file: str
    number_translation_nodes: int
    batch_size: int


@dataclass
class Config:
    basic_config: BasicConfig
    assistants: list[ChatAssistant]
    email_length_generator: NumberIntervalGenerator
    text_similarity_bounds: NumberInterval
    content_similarity_bounds: NumberInterval
    