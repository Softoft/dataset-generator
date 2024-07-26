from enum import Enum

from graph.nodes.state_full_node import save_state
from random_collections.random_collection_interface import IRandom
from graph.nodes.executable_node import ExecutableNode
from storage.key_value_storage import KeyValueStorage


class RandomCollectionNode[V: Enum](ExecutableNode):
    def __init__(self, value_type: type, parents, random_generator: IRandom):
        self.value_type = value_type
        self.random_generator = random_generator
        self.random_value = None
        super().__init__(parents)

    @save_state(lambda self: self.random_value)
    def execute(self, shared_storage: KeyValueStorage = None) -> KeyValueStorage:
        return super().execute(shared_storage)

    def _execute_node(self, shared_storage: KeyValueStorage) -> KeyValueStorage:
        self.random_value = self.random_generator.get_random_value()
        shared_storage.save(self.random_value)
        return shared_storage
