from enum import Enum

from graph.nodes.core.executable_node import ExecutableNode
from graph.nodes.core.save_execute_state import save_execute_state
from src.random_collections.random_collection_table import RandomTable
from storage.key_value_storage import KeyValueStorage


@save_execute_state(lambda self: self.random_value)
class RandomTableNode[K: Enum, V: Enum](ExecutableNode):
    def __init__(self, key_type: type, value_type: type, parents, random_generator: RandomTable[K, V]):
        self.key_type = key_type
        self.value_type = value_type
        self.random_generator = random_generator
        self.random_value = None
        super().__init__(parents)

    def _execute_node(self, shared_storage: KeyValueStorage) -> KeyValueStorage:
        key_value = shared_storage.load(self.key_type)
        self.random_value = self.random_generator.get_random_value(key_value)
        shared_storage.save(self.random_value)
        return shared_storage
