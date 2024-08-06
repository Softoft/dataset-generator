import pytest

from synthetic_data_generator.ai_graph.key_value_store import KeyValueStore
from tests.conftest import KeyEnum, ValueEnum


def test_enum_name():
    assert ValueEnum.__name__ == "ValueEnum"


def test_save_storage():
    storage = KeyValueStore()
    storage.save(ValueEnum.V1)

    assert storage.get(ValueEnum) == ValueEnum.V1


def test_raises_error_same_key():
    storage = KeyValueStore()
    storage.save(ValueEnum.V1)

    with pytest.raises(Exception):
        storage.save(ValueEnum.V2)


def test_raises_error_key_not_in_storage():
    storage = KeyValueStore()

    with pytest.raises(Exception):
        storage.get(ValueEnum)


def test_save_by_key():
    storage = KeyValueStore()
    storage.save_by_key("key1", ValueEnum.V1)

    assert storage.get_by_key("key1") == ValueEnum.V1


def test_merge():
    storage1 = KeyValueStore()
    storage1.save(KeyEnum.K1)

    storage2 = KeyValueStore()
    storage2.save(ValueEnum.V2)

    storage1.merge(storage2)

    assert storage1.get(ValueEnum) == ValueEnum.V2
    assert storage1.get(KeyEnum) == KeyEnum.K1


def test_merge_lists():
    storage1 = KeyValueStore()
    storage2 = KeyValueStore()

    storage1.save_by_key("key1", [1, 2])
    storage2.save_by_key("key1", [2, 3])

    storage1.merge(storage2)

    assert storage1.get_by_key("key1") == [1, 2, 2, 3]


def test_merge_sets():
    storage1 = KeyValueStore()
    storage2 = KeyValueStore()

    storage1.save_by_key("key1", { 1, 2 })
    storage2.save_by_key("key1", { 2, 3 })

    storage1.merge(storage2)

    assert storage1.get_by_key("key1") == { 1, 2, 3 }


def test_storage_contains():
    storage = KeyValueStore()
    storage.save(ValueEnum.V1)

    assert ValueEnum in storage
    assert KeyEnum not in storage

    storage.save(KeyEnum.K1)

    assert KeyEnum in storage
