from typing import Callable

from storage.key_value_storage import KeyValueStorage


def save_execute_state(instance_var_func: Callable[[object], any]):
    def class_decorator(cls):
        original_execute = cls.execute

        def wrapper(self, shared_storage: KeyValueStorage = None):
            instance_var_value = instance_var_func(self)
            shared_storage = shared_storage or KeyValueStorage()
            if instance_var_value:
                shared_storage.save(instance_var_value)
                return shared_storage
            return original_execute(self, shared_storage)

        cls.execute = wrapper
        return cls

    return class_decorator
