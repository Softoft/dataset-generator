from storage.key_value_storage import KeyValueStorage


def inject_storage_objects(*types):
    def decorator(func):
        def wrapper(self, shared_storage: KeyValueStorage):
            loaded_types = [shared_storage.load(type_) for type_ in types]
            return func(self, shared_storage, *loaded_types)

        return wrapper

    return decorator
