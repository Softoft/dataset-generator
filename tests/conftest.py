import asyncio
import logging
from enum import auto
from unittest.mock import Mock, create_autospec

import pytest
from openai import AsyncOpenAI, OpenAI
from openai.types.beta import AssistantResponseFormatParam
from openai.types.beta.threads import Run
from openai.types.beta.threads.run import Usage

from models import Ticket
from synthetic_data_generator.ai_graph.ai.chat_assistant import ChatAssistant
from synthetic_data_generator.ai_graph.ai.chat_assistant_analysis import AssistantAnalyzer, AssistantRun
from synthetic_data_generator.ai_graph.ai.chat_assistant_config import AssistantModel
from synthetic_data_generator.ai_graph.key_value_store import KeyValueStore
from synthetic_data_generator.ai_graph.nodes.executable_node import ExecutableNode
from synthetic_data_generator.random_generators.number_interval_generator import NormalizedNumberGenerator,\
    NumberInterval, NumberIntervalGenerator
from synthetic_data_generator.random_generators.random_collection import RandomCollectionFactory
from synthetic_data_generator.random_generators.random_collection_table import RandomTableBuilder
from synthetic_data_generator.random_nodes.random_collection_node import RandomCollectionNode
from synthetic_data_generator.random_nodes.random_table_node import RandomTableNode
from synthetic_data_generator.random_nodes.ticket_field import ComparableEnum
from ticket_extra_information_node import TicketExtraInformationNode
from ticket_rewriting_translating_node import TicketTranslationNode


class KeyEnum(ComparableEnum):
    K1 = auto()
    K2 = auto()


class ValueEnum(ComparableEnum):
    V1 = auto()
    V2 = auto()
    V3 = auto()


class BigEnum(ComparableEnum):
    B1 = auto()
    B2 = auto()
    B3 = auto()
    B4 = auto()
    B5 = auto()
    B6 = auto()


class ConfigurableEnumSaveNode(ExecutableNode):
    def __init__(self, key_enum_value: KeyEnum):
        self.key_enum_value = key_enum_value
        super().__init__([])

    async def _execute_node(self, shared_storage: KeyValueStore) -> KeyValueStore:
        if KeyEnum in shared_storage:
            return shared_storage
        shared_storage.save(self.key_enum_value)
        return shared_storage


@pytest.fixture(scope="session")
def chat_assistant_gpt4_o_mini():
    client = OpenAI()

    my_assistant = client.beta.assistants.create(
        instructions="You are a Simple Chatbot, Answer in short sentences.",
        name="Simple Chatbot",
        model="gpt-4o-mini",
    )

    yield ChatAssistant(client=AsyncOpenAI(), assistant_name="Simple Chatbot",
                        assistant_id=my_assistant.id,
                        model=AssistantModel.GPT_4o_MINI,
                        temperature=0.5)
    client.beta.assistants.delete(my_assistant.id)


@pytest.fixture()
def create_chat_assistant():
    client = OpenAI()
    chat_assistants = []

    def _create_chat_assistant(model: AssistantModel, instructions: str, assistant_name="Test Chatbot",
                               json_response: bool = False,
                               temperature: float = 0.5):
        if model == AssistantModel.GPT_4o:
            logging.error("GPT4o is expensive! Use GPT4o Mini for testing")
        my_assistant = client.beta.assistants.create(
            instructions=instructions,
            name=assistant_name,
            model=model.value,
            response_format=AssistantResponseFormatParam(type="json_object") if json_response else "auto",
        )

        test_chat_assistant = ChatAssistant(client=AsyncOpenAI(), assistant_name=assistant_name,
                                            assistant_id=my_assistant.id,
                                            model=AssistantModel.GPT_4o_MINI,
                                            temperature=temperature)
        chat_assistants.append(test_chat_assistant)
        return test_chat_assistant

    yield _create_chat_assistant

    for chat_assistant in chat_assistants:
        client.beta.assistants.delete(chat_assistant.assistant_id)


@pytest.fixture
def create_assistant_run():
    def _create_assistant_run(assistant_name, completion_tokens, prompt_tokens, model: AssistantModel):
        run = Mock(spec=Run)
        run.usage = Usage(completion_tokens=completion_tokens, prompt_tokens=prompt_tokens,
                          total_tokens=completion_tokens + prompt_tokens)
        run.model = model.value
        return AssistantRun(_run=run, assistant_name=assistant_name)

    return _create_assistant_run


@pytest.fixture
def create_mocked_assistant_run():
    def _create_mocked_assistant_run(completion_tokens, prompt_tokens, cost: float):
        run = create_autospec(AssistantRun, instance=True)
        run.assistant_name = "Test"
        run.model = AssistantModel.GPT_4o_MINI
        run.prompt_tokens = prompt_tokens
        run.completion_tokens = completion_tokens
        run.cost = cost
        return run

    return _create_mocked_assistant_run


@pytest.fixture(scope="session")
def chat_assistant_analyzer():
    yield AssistantAnalyzer()
    AssistantAnalyzer().reset()


@pytest.fixture
def create_enum_save_node():
    def _create_enum_save_node(key_enum_value: KeyEnum):
        return ConfigurableEnumSaveNode(key_enum_value)

    return _create_enum_save_node


@pytest.fixture
def create_random_table_node(create_enum_save_node):
    def _create_random_table_node(key_value, table_weight_dict):
        random_table = RandomTableBuilder.build_from_dict(KeyEnum, ValueEnum, table_weight_dict)
        return RandomTableNode(KeyEnum, ValueEnum, [create_enum_save_node(key_value)], random_table)

    return _create_random_table_node


@pytest.fixture
def create_random_collection_node():
    def _create_random_collection_node(value_weight_dict):
        random_collection = RandomCollectionFactory.build_from_value_weight_dict(value_weight_dict)
        return RandomCollectionNode(ValueEnum, [], random_collection)

    return _create_random_collection_node


@pytest.fixture
def create_random_number_generator():
    def _create_random_number_generator(mean: int, standard_deviation: int, number_bounds: NumberInterval):
        return NormalizedNumberGenerator(mean=mean, standard_deviation=standard_deviation, number_bounds=number_bounds)

    return _create_random_number_generator


@pytest.fixture
def get_random_numbers(create_random_number_generator):
    def _get_random_numbers(mean, standard_deviation, number_bounds=None, amount: int = 10_000):
        random_number_generator = create_random_number_generator(mean, standard_deviation, number_bounds)
        return [random_number_generator.generate_bounded_number() for _ in range(amount)]

    return _get_random_numbers


@pytest.fixture
def get_mocked_random_interval():
    def _get_mocked_random_interval(lower_value, min_upper_bound_difference):
        normalized_number_generator = Mock(spec=NormalizedNumberGenerator)
        normalized_number_generator.generate_bounded_number.return_value = lower_value

        return NumberIntervalGenerator(mean=0, standard_deviation=1,
                                       min_upper_bound_difference=min_upper_bound_difference,
                                       lower_number_generator=normalized_number_generator)

    return _get_mocked_random_interval


@pytest.fixture
def create_key_value_store():
    def _create_key_value_store(*stored_values):
        key_value_store = KeyValueStore()
        for value in stored_values:
            key_value_store.save(value)
        return key_value_store

    return _create_key_value_store


@pytest.fixture
def extra_ticket_information_node():
    return TicketExtraInformationNode()


@pytest.fixture
def create_answer_ticket_node():
    def _create_answer_ticket_node():
        return None

    return _create_answer_ticket_node


@pytest.fixture
def execute_ticket_translation_node():
    async def _create_ticket_translation_node_for_ticket(ticket: Ticket):
        shared_storage = KeyValueStore()
        shared_storage.save(ticket)
        ticket_translation_node = TicketTranslationNode([])
        return await ticket_translation_node.execute(shared_storage)

    return _create_ticket_translation_node_for_ticket


@pytest.fixture(autouse=True)
def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
