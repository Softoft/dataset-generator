import json
from pathlib import Path

from openai import AsyncOpenAI

from config.config import BasicConfig, Config
from synthetic_data_generator.ai_graph.ai.chat_assistant import ChatAssistant
from synthetic_data_generator.random_generators.number_interval_generator import NormalizedNumberGenerator,\
    NumberInterval, NumberIntervalGenerator


class ConfigLoader:
    def __init__(self, config_file: Path, async_openai: AsyncOpenAI):
        self.config_file = config_file
        self.async_openai = async_openai

    def load_config(self) -> Config:
        json_data = json.loads(self.config_file.read_text())
        basic_config = BasicConfig(**json_data['basic'])

        assistants_data = json_data['assistants']
        assistants = [ChatAssistant(client=self.async_openai, **assistant_data) for assistant_data in assistants_data]

        email_length_generator = NumberIntervalGenerator(**json_data['text_length'],
                                                         lower_number_generator=NormalizedNumberGenerator())

        text_similarity_bounds = NumberInterval(**json_data['text_similarity_bounds'])
        content_similarity_bounds = NumberInterval(**json_data['content_similarity_bounds'])

        return Config(
            basic_config=basic_config,
            assistants=assistants,
            email_length_generator=email_length_generator,
            text_similarity_bounds=text_similarity_bounds,
            content_similarity_bounds=content_similarity_bounds
        )
