from typing import Self


class KeyValueStore:
    def __init__(self, *values: any):
        self.storage: dict[str, any] = { }
        self.save(*values)

    def __contains__(self, key: type) -> bool:
        if not isinstance(key, type):
            raise ValueError(f"Key must be a type, not {type(key).__name__}")
        return key.__name__ in self.storage

    def save(self, *values: any) -> None:
        for value in values:
            key = type(value).__name__
            self.save_by_key(key, value)

    def get(self, value_type: type) -> any:
        key = value_type.__name__
        return self.get_by_key(key)

    def save_by_key(self, key: str, value: any) -> None:
        if key in self.storage:
            raise ValueError(f"Key {key} already exists in storage")
        self.storage[key] = value

    def get_by_key(self, key: str) -> any:
        if key not in self.storage:
            raise KeyError(f"Key {key} not found in storage")
        return self.storage[key]

    def merge(self, *storages: Self) -> None:
        for storage in storages:
            for key, value in storage.storage.items():
                if key not in self.storage:
                    self.storage[key] = value
                else:
                    self._merge_value(key, value)

    def _merge_value(self, key: str, value: any) -> None:
        stored_value = self.storage[key]
        if isinstance(stored_value, list) and isinstance(value, list):
            stored_value += value
        elif isinstance(stored_value, set) and isinstance(value, set):
            stored_value.update(value)
        else:
            raise ValueError(f"Conflict merging key {key}: incompatible types")


def inject_storage_objects(*types: type):
    def decorator(func):
        def wrapper(self, shared_storage: KeyValueStore):
            loaded_types = [shared_storage.get(type_) for type_ in types]
            return func(self, shared_storage, *loaded_types)

        return wrapper

    return decorator
