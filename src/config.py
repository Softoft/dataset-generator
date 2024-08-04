from dataclasses import dataclass

from ai.chat_assistant import ChatAssistantConfig
from util.number_interval_generator import NumberIntervalGenerator
from util.text_similarity_calculator import TicketParaphraseValidator


@dataclass
class BasicConfig:
    number_of_tickets: int
    output_file: str
    number_translation_nodes: int
    batch_size: int


@dataclass
class Config:
    basic_config: BasicConfig
    assistants: list[ChatAssistantConfig]
    email_length_generator: NumberIntervalGenerator
    ticket_paraphrase_validator: TicketParaphraseValidator
