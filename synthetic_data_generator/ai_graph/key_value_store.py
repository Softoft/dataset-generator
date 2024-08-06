from typing import Self


class KeyValueStore:
    def __init__(self, *values: any):
        self.storage: dict[str, object] = { }
        self.save(*values)

    def __contains__(self, key: type) -> bool:
        if not isinstance(key, type):
            raise ValueError(f"Key must be a type, not {type(key)}")
        return key.__name__ in self.storage

    def save(self, *values: any) -> None:
        for value in values:
            key = type(value).__name__
            if key in self.storage:
                raise ValueError(f"Key {key} already exists in storage")
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


def inject_storage_objects(*types):
    def decorator(func):
        def wrapper(self, shared_storage: KeyValueStore):
            loaded_types = [shared_storage.get(type_) for type_ in types]
            return func(self, shared_storage, *loaded_types)

        return wrapper

    return decorator
