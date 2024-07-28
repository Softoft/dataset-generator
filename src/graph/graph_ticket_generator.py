from graph.data.models import Ticket, TicketType
from graph.key_value_storage import KeyValueStorage
from graph.node_factories.ticket_queue_priority_node import create_queue_priority_node
from graph.node_factories.ticket_type_queue_node_factory import create_ticket_type_queue_node
from graph.nodes.core.executable_node import ExecutableNode
from graph.nodes.core.random_collection_node import RandomCollectionNode
from graph.nodes.text_length_node import TextLengthGenerator, TextLengthNode
from graph.nodes.ticket_answer_node import TicketAnswerNode
from graph.nodes.ticket_email_node import TicketEmailNode
from graph.nodes.ticket_extra_information_node import TicketExtraInformationNode
from graph.nodes.ticket_rewriting_and_translating_node import TicketTranslationNode
from random_collections.random_collection import RandomCollectionBuilder


def create_text_length_node(mean: int, standard_deviation: int) -> TextLengthNode:
    text_length_generator = TextLengthGenerator(mean=mean, standard_deviation=standard_deviation)
    return TextLengthNode(text_length_generator)


def create_ticket_type_node() -> RandomCollectionNode:
    ticket_type_collection = RandomCollectionBuilder.build_from_value_weight_dict(
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

    async def _execute_node(self, shared_storage: KeyValueStorage) -> KeyValueStorage:
        return shared_storage


class GraphTicketGenerator:
    def __init__(self, ticket_text_length_mean=250, ticket_text_length_standard_deviation=400):
        self.ticket_type_node = create_ticket_type_node()
        self.ticket_queue_node = create_ticket_type_queue_node(self.ticket_type_node)
        self.ticket_queue_priority_node = create_queue_priority_node(self.ticket_queue_node)
        self.text_length_node = create_text_length_node(mean=ticket_text_length_mean,
                                                        standard_deviation=ticket_text_length_standard_deviation)
        self.ticket_extra_information_node = TicketExtraInformationNode([self.ticket_type_node, self.ticket_queue_node])
        self.ticket_email_generator_node = TicketEmailNode(
            [self.ticket_extra_information_node, self.ticket_queue_priority_node, self.text_length_node])
        self.ticket_answer_node = TicketAnswerNode([self.ticket_email_generator_node])
        self.ticket_translation_node1 = TicketTranslationNode([self.ticket_answer_node])
        self.ticket_translation_node2 = TicketTranslationNode([self.ticket_answer_node])
        self.ticket_translation_node3 = TicketTranslationNode([self.ticket_answer_node])
        self.ticket_translation_node4 = TicketTranslationNode([self.ticket_answer_node])

        self.end_node = EndNode(
            [self.ticket_translation_node1, self.ticket_translation_node2, self.ticket_translation_node3,
             self.ticket_translation_node4])

    async def create_translated_ticket(self):
        shared_storage = await self.end_node.execute()
        return shared_storage.get(Ticket)