import asyncio

from synthetic_data_generator.ai_graph.key_value_store import KeyValueStore
from synthetic_data_generator.ai_graph.nodes.executable_node import ExecutableNode
from synthetic_data_generator.ai_graph.nodes.inject_storage_objects import inject_storage_objects
from tests.conftest import KeyEnum, ValueEnum


class MyExecutableNode(ExecutableNode):
    def __init__(self, parents):
        self.execute_count = 0
        super().__init__(parents)

    async def _execute_node(self, shared_storage: KeyValueStore) -> KeyValueStore:
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


def test_shared_storage(create_enum_save_node):
    key_value = KeyEnum.K2
    node = MyExecutableNode([create_enum_save_node(key_value)])
    storage: KeyValueStore = asyncio.run(node.execute())

    value_enum_loaded = storage.get(ValueEnum)
    key_enum_loaded = storage.get(KeyEnum)

    assert value_enum_loaded == ValueEnum.V1
    assert key_enum_loaded == key_value


def test_inject_storage_decorator():
    shared_storage = KeyValueStore(KeyEnum.K1, ValueEnum.V1)

    @inject_storage_objects(KeyEnum, ValueEnum)
    def decorated_func(_shared_storage, key_enum: KeyEnum, value_enum: ValueEnum):
        assert key_enum == KeyEnum.K1
        assert value_enum == ValueEnum.V1

    decorated_func(shared_storage)
