import asyncio

from src.graph.executable_node import ExecutableNode
from src.graph.storage import KeyValueStorage
from tests.conftest import KeyEnum, ValueEnum


class EnumSaveNode(ExecutableNode):
	def __init__(self, parents):
		super().__init__(parents)

	async def _execute_node(self, shared_storage: KeyValueStorage) -> KeyValueStorage:
		if KeyEnum in shared_storage:
			return shared_storage
		shared_storage.save(KeyEnum.K2)
		return shared_storage


class MyExecutableNode(ExecutableNode):
	def __init__(self, parents):
		self.execute_count = 0
		super().__init__(parents)

	async def _execute_node(self, shared_storage: KeyValueStorage) -> KeyValueStorage:
		self.execute_count += 1
		if ValueEnum in shared_storage:
			return shared_storage
		shared_storage.save(ValueEnum.V1)
		return shared_storage


def test_execute_node():
	node = MyExecutableNode([])
	asyncio.run(node.execute())
	assert node.execute_count == 1

	asyncio.run(node.execute())
	assert node.execute_count == 1


def test_execute_parents():
	parent: MyExecutableNode = MyExecutableNode([])
	node = MyExecutableNode([parent])

	asyncio.run(node.execute())
	assert parent.execute_count == 1
	assert node.execute_count == 1


def test_shared_storage():
	parent = EnumSaveNode([])
	node = MyExecutableNode([parent])
	storage: KeyValueStorage = asyncio.run(node.execute())

	value_enum_loaded = storage.load(ValueEnum)
	key_enum_loaded = storage.load(KeyEnum)

	print(f"value_enum_loaded: {value_enum_loaded}, type: {type(value_enum_loaded)}")
	print(f"key_enum_loaded: {key_enum_loaded}, type: {type(key_enum_loaded)}")

	assert value_enum_loaded == ValueEnum.V1
	assert key_enum_loaded == KeyEnum.K2
