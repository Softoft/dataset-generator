import copy
from typing import Self


class KeyValueStorage:
    def __init__(self):
        self.storage: dict[str, any] = {}

    def save(self, value: any):
        self.storage[type(value).__name__] = value

    def load(self, value_type: type) -> any:
        return self.storage[value_type.__name__]

    def merge(self, storages: list[Self]):
        for storage in storages:
            self.storage.update(storage.storage)

    def deepcopy(self):
        new_storage = KeyValueStorage()
        new_storage.storage = copy.deepcopy(self.storage)
        return new_storage
