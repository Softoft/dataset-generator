from graph.nodes.random_collection_node import RandomCollectionNode
from graph.data.ticket_type import TicketType
from random_collections.random_collection import RandomCollectionBuilder


def create_ticket_type_node() -> RandomCollectionNode:
    ticket_type_collection = RandomCollectionBuilder.build_from_value_weight_dict(
        {
            TicketType.INCIDENT: 4,
            TicketType.REQUEST: 3,
            TicketType.PROBLEM: 2,
            TicketType.CHANGE: 1
        })

    return RandomCollectionNode(TicketType, [], ticket_type_collection)
