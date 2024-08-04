from tests.conftest import KeyEnum, ValueEnum
from util.key_value_storage import KeyValueStore


def test_enum_name():
    assert ValueEnum.__name__ == "ValueEnum"


def test_save_storage():
    storage = KeyValueStore()
    storage.save(ValueEnum.V1)

    assert storage.get(ValueEnum) == ValueEnum.V1


def test_storage_contains():
    storage = KeyValueStore()
    storage.save(ValueEnum.V1)

    assert ValueEnum in storage
    assert KeyEnum not in storage

    storage.save(KeyEnum.K1)

    assert KeyEnum in storage
