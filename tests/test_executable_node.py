import asyncio

from src.graph.executable_node import ExecutableNode
from src.graph.storage import KeyValueStorage
from tests.conftest import KeyEnum, ValueEnum


class EnumSaveNode(ExecutableNode):
    def __init__(self, parents):
        super().__init__(parents)

    async def _execute_node(self, shared_storage: KeyValueStorage) -> KeyValueStorage:
        shared_storage.save(KeyEnum.K2)
        return shared_storage


class MyExecutableNode(ExecutableNode):
    def __init__(self, parents):
        self.execute_count = 0
        super().__init__(parents)

    async def _execute_node(self, shared_storage: KeyValueStorage) -> KeyValueStorage:
        self.execute_count += 1
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

    assert storage.load(ValueEnum) == ValueEnum.V1
    assert storage.load(KeyEnum) == KeyEnum.K2
