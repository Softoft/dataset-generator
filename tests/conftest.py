import asyncio
import logging
from enum import auto
from unittest.mock import Mock

import pytest
from graph.data.ticket_field import ComparableEnum
from graph.nodes.core.executable_node import ExecutableNode
from graph.nodes.core.random_collection_node import RandomCollectionNode
from graph.nodes.core.random_table_node import RandomTableNode
from graph.nodes.ticket_extra_information_node import TicketExtraInformationNode
from graph.nodes.ticket_rewriting_translating_node import TicketTranslationNode
from synthetic_data_generator.ai_graph.data.models import NumberInterval, Ticket

from synthetic_data_generator.ai_graph.key_value_store import KeyValueStore
from synthetic_data_generator.random_generators.number_interval_generator import NormalizedNumberGenerator,\
    NumberIntervalGenerator
from synthetic_data_generator.random_generators.random_collection import RandomCollectionFactory
from synthetic_data_generator.random_generators.random_collection_table import RandomTableBuilder


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
