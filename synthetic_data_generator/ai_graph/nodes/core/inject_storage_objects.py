from synthetic_data_generator.ai_graph.key_value_store import KeyValueStore


def inject_storage_objects(*types):
    def decorator(func):
        def wrapper(self, shared_storage: KeyValueStore):
            loaded_types = [shared_storage.get(type_) for type_ in types]
            return func(self, shared_storage, *loaded_types)

        return wrapper

    return decorator
