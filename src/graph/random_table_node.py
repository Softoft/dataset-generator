from enum import Enum

from src.graph.executable_node import ExecutableNode
from src.graph.storage import KeyValueStorage
from src.random_collections.random_collection_table import RandomTable


class RandomTableNode[K: Enum, V: Enum](ExecutableNode):
    def __init__(self, key_type: type, value_type: type, parents, random_generator: RandomTable[K, V]):
        self.key_type = key_type
        self.value_type = value_type
        self.random_generator = random_generator
        self.random_value = None
        super().__init__(parents)

    async def execute(self, shared_storage: KeyValueStorage = None) -> KeyValueStorage:
        shared_storage = shared_storage or KeyValueStorage()
        if self.random_value:
            if type(self.random_value) not in shared_storage:
                shared_storage.save(self.random_value)
            return shared_storage
        return await super().execute(shared_storage)

    async def _execute_node(self, shared_storage: KeyValueStorage) -> KeyValueStorage:
        key_value = shared_storage.load(self.key_type)
        self.random_value = self.random_generator.get_random_value(key_value)
        shared_storage.save(self.random_value)
        return shared_storage