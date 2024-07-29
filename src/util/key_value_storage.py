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

    def get(self, value_type: type) -> any:
        return self.storage[value_type.__name__]

    def save_by_key(self, key: str, value: any) -> None:
        self.storage[key] = value

    def get_by_key(self, key: str) -> any:
        return self.storage[key]

    def merge(self, storages: list[Self]) -> None:
        for storage in storages:
            for key, value in storage.storage.items():
                if key in self.storage and isinstance(self.storage[key], list) and isinstance(value, list):
                    self.storage[key] += value
                else:
                    self.storage[key] = value

    def deepcopy(self) -> Self:
        new_storage = KeyValueStorage()
        new_storage.storage = copy.deepcopy(self.storage)
        return new_storage
