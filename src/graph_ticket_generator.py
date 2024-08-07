from dataclasses import dataclass

from config import Config
from models import TicketType
from synthetic_data_generator.ai_graph.key_value_store import KeyValueStore
from synthetic_data_generator.ai_graph.nodes.executable_node import ExecutableNode
from synthetic_data_generator.random_generators.random_collection import RandomCollectionFactory
from synthetic_data_generator.random_nodes.random_collection_node import RandomCollectionNode


def create_ticket_type_node() -> RandomCollectionNode:
    ticket_type_collection = RandomCollectionFactory().build_from_value_weight_dict(
        {
            TicketType.INCIDENT: 4,
            TicketType.REQUEST: 3,
            TicketType.PROBLEM: 2,
            TicketType.CHANGE: 1
        })

    return RandomCollectionNode(TicketType, [], ticket_type_collection)


class EndNode(ExecutableNode):
    def __init__(self, parents: list):
        super().__init__(parents)

    async def _execute_node(self, shared_storage: KeyValueStore) -> KeyValueStore:
        return shared_storage


@dataclass
class GraphTicketGenerator:
    config: Config
