from enum import Enum

from random_collections.random_collection_interface import IRandom
from src.graph.executable_node import ExecutableNode
from src.graph.storage import KeyValueStorage


class RandomCollectionNode[V: Enum](ExecutableNode):
    def __init__(self, value_type: type, parents, random_generator: IRandom):
        self.value_type = value_type
        self.random_generator = random_generator
        self.random_value = None
        super().__init__(parents)

    async def execute(self, shared_storage: KeyValueStorage = None) -> KeyValueStorage:
        shared_storage = shared_storage or KeyValueStorage()
        if self.random_value:
            shared_storage.save(self.random_value)
            return shared_storage
        return await super().execute(shared_storage)

    async def _execute_node(self, shared_storage: KeyValueStorage) -> KeyValueStorage:
        self.random_value = self.random_generator.get_random_value()
        shared_storage.save(self.random_value)
        return shared_storage
