from dataclasses import dataclass

from config import Config
from models import Ticket, TicketType
from synthetic_data_generator.ai_graph.key_value_store import KeyValueStore
from synthetic_data_generator.ai_graph.nodes.core.executable_node import ExecutableNode
from synthetic_data_generator.random_collection_node import RandomCollectionNode
from synthetic_data_generator.random_generators.random_collection import RandomCollectionFactory
from ticket_answer_node import TicketAnswerNode
from ticket_email_node import TicketEmailNode
from ticket_extra_information_node import TicketExtraInformationNode
from ticket_queue_priority_node import create_queue_priority_node
from ticket_rewriting_translating_node import TicketTranslationNode
from ticket_type_queue_node_factory import create_ticket_type_queue_node


def create_ticket_type_node() -> RandomCollectionNode:
    ticket_type_collection = RandomCollectionFactory.build_from_value_weight_dict(
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

    def __post_init__(self):
        self.ticket_type_node = create_ticket_type_node()
        self.ticket_queue_node = create_ticket_type_queue_node(self.ticket_type_node)
        self.ticket_queue_priority_node = create_queue_priority_node(self.ticket_queue_node)
        self.ticket_extra_information_node = TicketExtraInformationNode(
            [self.ticket_type_node, self.ticket_queue_node, self.ticket_queue_priority_node])
        self.ticket_email_generator_node = TicketEmailNode(
            [self.ticket_extra_information_node, self.ticket_queue_priority_node])
        self.ticket_answer_node = TicketAnswerNode([self.ticket_email_generator_node])
        self.ticket_translation_nodes = self._create_ticket_translation_nodes()

        self.end_node = EndNode(self.ticket_translation_nodes)

    def _create_ticket_translation_nodes(self) -> list[TicketTranslationNode]:
        return [TicketTranslationNode([self.ticket_answer_node]) for _ in range(self.config.number_translation_nodes)]

    async def create_translated_tickets(self) -> list[Ticket]:
        shared_storage = await self.end_node.execute()
        return shared_storage.get_by_key("tickets")
