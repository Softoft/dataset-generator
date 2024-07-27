from graph.nodes.core.executable_node import ExecutableNode
from graph.key_value_storage import KeyValueStorage
from tests.conftest import KeyEnum, ValueEnum


class MyExecutableNode(ExecutableNode):
    def __init__(self, parents):
        self.execute_count = 0
        super().__init__(parents)

    def _execute_node(self, shared_storage: KeyValueStorage) -> KeyValueStorage:
        self.execute_count += 1
        if ValueEnum in shared_storage:
            return shared_storage
        shared_storage.save(ValueEnum.V1)
        return shared_storage


def test_execute_node():
    node = MyExecutableNode([])
    node.execute()
    assert node.execute_count == 1

    node.execute()
    assert node.execute_count == 1


def test_execute_parents():
    parent: MyExecutableNode = MyExecutableNode([])
    node = MyExecutableNode([parent])

    node.execute()
    assert parent.execute_count == 1
    assert node.execute_count == 1


def test_shared_storage(create_enum_save_node):
    key_value = KeyEnum.K2
    node = MyExecutableNode([create_enum_save_node(key_value)])
    storage: KeyValueStorage = node.execute()

    value_enum_loaded = storage.load(ValueEnum)
    key_enum_loaded = storage.load(KeyEnum)

    assert value_enum_loaded == ValueEnum.V1
    assert key_enum_loaded == key_value
