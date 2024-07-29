from enum import Enum

from graph.nodes.core.executable_node import ExecutableNode
from random_collections.random_collection_interface import IRandom
from util.key_value_storage import KeyValueStorage


class RandomCollectionNode[V: Enum](ExecutableNode):
    def __init__(self, value_type: type, parents, random_generator: IRandom):
        self.value_type = value_type
        self.random_generator = random_generator
        super().__init__(parents)

    async def _execute_node(self, shared_storage: KeyValueStorage) -> KeyValueStorage:
        shared_storage.save(self.random_generator.get_random_value())
        return shared_storage
