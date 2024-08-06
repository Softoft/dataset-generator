from enum import Enum

from synthetic_data_generator.ai_graph.key_value_store import KeyValueStore
from synthetic_data_generator.ai_graph.nodes.executable_node import ExecutableNode, INode
from synthetic_data_generator.random_generators.random_collection_table import RandomTable


class RandomTableNode[K: Enum, V: Enum](ExecutableNode):
    def __init__(self, key_type: type, value_type: type, parents: list[INode], random_generator: RandomTable[K, V]):
        self.key_type = key_type
        self.value_type = value_type
        self.random_generator = random_generator
        super().__init__(parents)

    async def _execute_node(self, shared_storage: KeyValueStore) -> KeyValueStore:
        key_value = shared_storage.get(self.key_type)
        shared_storage.save(self.random_generator.get_random_value(key_value))
        return shared_storage
