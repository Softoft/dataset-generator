from src.graph.storage import KeyValueStorage
from tests.conftest import ValueEnum


def test_enum_name():
    assert ValueEnum.__name__ == "ValueEnum"


def test_node_storage():
    storage = KeyValueStorage()
    storage.save(ValueEnum.V1)

    assert storage.load(ValueEnum) == ValueEnum.V1

    storage.save(ValueEnum.V2)

    assert storage.load(ValueEnum) == ValueEnum.V2
