import logging

import pytest

from graph.data.category_ticket_field import ComparableEnum
from graph.graph_ticket_generator import GraphTicketGenerator
from graph.key_value_storage import KeyValueStorage
from graph.nodes.core.executable_node import ExecutableNode
from graph.nodes.core.random_collection_node import RandomCollectionNode
from graph.nodes.core.random_table_node import RandomTableNode
from graph.nodes.text_length_node import TextLengthNode
from graph.nodes.ticket_extra_information_node import TicketExtraInformationNode
from random_collections.random_collection import RandomCollectionBuilder
from random_collections.random_collection_table import RandomTableBuilder
from text_length_generator import TextLengthGenerator


class KeyEnum(ComparableEnum):
    K1 = 1
    K2 = 2


class ValueEnum(ComparableEnum):
    V1 = 1
    V2 = 2
    V3 = 3


class ConfigurableEnumSaveNode(ExecutableNode):
    def __init__(self, key_enum_value: KeyEnum):
        self.key_enum_value = key_enum_value
        super().__init__([])

    async def _execute_node(self, shared_storage: KeyValueStorage) -> KeyValueStorage:
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
        random_collection = RandomCollectionBuilder.build_from_value_weight_dict(value_weight_dict)
        return RandomCollectionNode(ValueEnum, [], random_collection)

    return _create_random_collection_node


@pytest.fixture
def create_text_length_node():
    def _create_text_length_node(mean, standard_deviation):
        text_length_generator = TextLengthGenerator(mean=mean, standard_deviation=standard_deviation)
        return TextLengthNode(text_length_generator)

    return _create_text_length_node


@pytest.fixture
def create_extra_ticket_information_node():
    def _create_extra_ticket_information_node():
        graph = GraphTicketGenerator()
        return TicketExtraInformationNode([graph.ticket_queue_node, graph.ticket_type_node])

    return _create_extra_ticket_information_node


@pytest.fixture
def create_answer_ticket_node():
    def _create_answer_ticket_node():
        graph = GraphTicketGenerator()
        return graph.ticket_answer_node

    return _create_answer_ticket_node


@pytest.fixture
def create_ticket_translation_node():
    def _create_ticket_translation_node():
        graph = GraphTicketGenerator()
        return graph.ticket_translation_node

    return _create_ticket_translation_node


@pytest.fixture(autouse=True)
def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
