import dataclasses
import json
from pathlib import Path
from unittest.mock import Mock

from config.config import BasicConfig, Config
from config.config_loader import ConfigLoader
from synthetic_data_generator.ai_graph.ai.chat_assistant import ChatAssistant
from synthetic_data_generator.ai_graph.ai.chat_assistant_config import AssistantModel
from synthetic_data_generator.random_generators.number_interval_generator import NumberInterval, NumberIntervalGenerator

test_config = Config(
    basic_config=BasicConfig(
        number_of_tickets=10,
        output_file="test.json",
        number_translation_nodes=5,
        batch_size=5
    ),
    text_similarity_bounds=NumberInterval(lower_bound=0.5, upper_bound=0.9),
    content_similarity_bounds=NumberInterval(lower_bound=0.5, upper_bound=0.9),
    email_length_generator=NumberIntervalGenerator(
        mean=100,
        standard_deviation=10,
        min_upper_bound_difference=10,
        lower_number_bounds=NumberInterval.get_positive_interval(),
        lower_number_generator=Mock()
    ),
    assistants=[
        ChatAssistant(assistant_name="Test Chatbot", assistant_id="test_id", model=AssistantModel.GPT_4o_MINI,
                      temperature=0.5,
                      client=Mock())
    ],
)


def test_load_config():
    config_file = Mock(spec=Path)
    config_file.read_text.return_value = json.dumps(dataclasses.asdict(test_config))
    config_loader = ConfigLoader(config_file, Mock())
    config = config_loader.load_config()
