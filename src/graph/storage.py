import copy
from typing import Self


class KeyValueStorage:
    def __init__(self):
        self.storage: dict[str, object] = {}

    def __contains__(self, key: type) -> bool:
        if not isinstance(key, type):
            raise ValueError(f"Key must be a type, not {type(key)}")
        return key.__name__ in self.storage

    def save(self, value: any) -> None:
        key = type(value).__name__
        self.storage[key] = value

    def load(self, value_type: type) -> any:
        return self.storage[value_type.__name__]

    def merge(self, storages: list[Self]) -> None:
        for storage in storages:
            self.storage.update(storage.storage)

    def deepcopy(self) -> Self:
        new_storage = KeyValueStorage()
        new_storage.storage = copy.deepcopy(self.storage)
        return new_storage
