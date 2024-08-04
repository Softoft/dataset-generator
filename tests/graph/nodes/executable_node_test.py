import asyncio

from graph.nodes.core.executable_node import ExecutableNode

from synthetic_data_generator.ai_graph.key_value_store import KeyValueStore
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
