from enum import Enum

import pytest

from graph.executable_node import ExecutableNode
from graph.random_node import RandomTableNode
from graph.storage import KeyValueStorage
from random_collections.random_collection_table import RandomTableBuilder


class KeyEnum(Enum):
	K1 = 1
	K2 = 2


class ValueEnum(Enum):
	V1 = 1
	V2 = 2
	V3 = 3


class KeyEnumSaveNode(ExecutableNode):
	def __init__(self, parents):
		super().__init__(parents)

	async def _execute_node(self, shared_storage: KeyValueStorage) -> KeyValueStorage:
		if KeyEnum in shared_storage:
			return shared_storage
		shared_storage.save(KeyEnum.K2)
		return shared_storage


@pytest.fixture
def random_table_node():
	random_table = RandomTableBuilder.build_from_dict(
		KeyEnum, ValueEnum,
		{
			KeyEnum.K1: { ValueEnum.V1: 0.5, ValueEnum.V2: 0.5, ValueEnum.V3: 0 },
			KeyEnum.K2: { ValueEnum.V1: 0, ValueEnum.V2: 1, ValueEnum.V3: 0 },
		}
	)
	random_table_node = RandomTableNode([KeyEnumSaveNode([])], random_table)
	return random_table_node
