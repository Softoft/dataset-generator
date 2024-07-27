from graph.data.language import Language
from graph.data.ticket_type import TicketType
from graph.node_factories.ticket_queue_priority_node import create_queue_priority_node
from graph.node_factories.ticket_type_queue_node_factory import create_ticket_type_queue_node
from graph.nodes.core.random_collection_node import RandomCollectionNode
from graph.nodes.text_length_node import TextLengthNode
from graph.nodes.ticket_email_node import TicketEmailNode
from graph.nodes.ticket_extra_information_node import TicketExtraInformationNode
from random_collections.random_collection import RandomCollectionBuilder
from random_collections.random_collection_interface import IRandom
from text_length_generator import TextLengthGenerator


class Graph:
    def __init__(self, ticket_text_length_mean=250, ticket_text_length_standard_deviation=400):
        self.ticket_type_node = self.create_ticket_type_node()
        self.ticket_queue_node = create_ticket_type_queue_node(self.ticket_type_node)
        self.ticket_queue_priority_node = create_queue_priority_node(self.ticket_queue_node)
        self.language_node = self.create_language_node()
        self.text_length_node = self.create_text_length_node(mean=ticket_text_length_mean,
                                                             standard_deviation=ticket_text_length_standard_deviation)
        self.ticket_extra_information_node = TicketExtraInformationNode([self.ticket_type_node, self.ticket_queue_node])
        self.ticket_email_generator_node = TicketEmailNode(
            [self.ticket_extra_information_node, self.ticket_queue_priority_node, self.language_node,
             self.text_length_node])

    def create_text_length_node(self, mean: int, standard_deviation: int) -> TextLengthNode:
        text_length_generator = TextLengthGenerator(mean=mean, standard_deviation=standard_deviation)
        return TextLengthNode(text_length_generator)

    def create_language_node(self) -> RandomCollectionNode:
        random_language_collection: IRandom = RandomCollectionBuilder.build_from_value_weight_dict(
            { Language.DE: 2, Language.EN: 4, Language.FR: 1, Language.ES: 2 })

        return RandomCollectionNode(Language, [], random_language_collection)

    def create_ticket_type_node(self) -> RandomCollectionNode:
        ticket_type_collection = RandomCollectionBuilder.build_from_value_weight_dict(
            {
                TicketType.INCIDENT: 4,
                TicketType.REQUEST: 3,
                TicketType.PROBLEM: 2,
                TicketType.CHANGE: 1
            })

        return RandomCollectionNode(TicketType, [], ticket_type_collection)
