from enum import Enum

from synthetic_data_generator.ai_graph.key_value_store import KeyValueStore
from synthetic_data_generator.ai_graph.nodes.core.executable_node import ExecutableNode
from synthetic_data_generator.random_generators.random_collection_interface import IRandom


class RandomCollectionNode[V: Enum](ExecutableNode):
    def __init__(self, value_type: type, parents, random_generator: IRandom):
        self.value_type = value_type
        self.random_generator = random_generator
        super().__init__(parents)

    async def _execute_node(self, shared_storage: KeyValueStore) -> KeyValueStore:
        shared_storage.save(self.random_generator.get_random_value())
        return shared_storage
