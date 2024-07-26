from storage.key_value_storage import KeyValueStorage
from tests.conftest import KeyEnum, ValueEnum


def test_enum_name():
    assert ValueEnum.__name__ == "ValueEnum"


def test_save_storage():
    storage = KeyValueStorage()
    storage.save(ValueEnum.V1)

    assert storage.load(ValueEnum) == ValueEnum.V1


def test_storage_contains():
    storage = KeyValueStorage()
    storage.save(ValueEnum.V1)

    assert ValueEnum in storage
    assert KeyEnum not in storage

    storage.save(KeyEnum.K1)

    assert KeyEnum in storage
