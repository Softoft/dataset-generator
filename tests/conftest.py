import logging

import pytest

from graph.executable_node import ExecutableNode
from graph.random_collection_node import RandomCollectionNode
from graph.random_table_node import RandomTableNode
from graph.storage import KeyValueStorage
from random_collections.random_collection import RandomCollectionBuilder
from random_collections.random_collection_table import RandomTableBuilder
from ticket_fields.category_ticket_field import ComparableEnum


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


@pytest.fixture(autouse=True)
def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
