from graph.core.random_collection_node import RandomCollectionNode
from graph.core.random_table_node import RandomTableNode
from graph.data.language import Language
from graph.data.priority import Priority
from graph.data.queue import TicketQueue
from graph.data.ticket_type import TicketType
from random_collections.random_collection import RandomCollectionBuilder
from random_collections.random_collection_interface import IRandom
from random_collections.random_collection_table import RandomTable, RandomTableBuilder


class Graph:
    def __init__(self):
        self.ticket_type_node = self.create_ticket_type_node()
        self.ticket_queue_node = self.create_ticket_type_queue_node(self.ticket_type_node)
        self.ticket_queue_priority_node = self.create_queue_priority_node(self.ticket_queue_node)
        self.language_node = self.create_language_node()

    def create_ticket_type_node(self) -> RandomCollectionNode:
        ticket_type_collection = RandomCollectionBuilder.build_from_value_weight_dict(
            {
                TicketType.INCIDENT: 4,
                TicketType.REQUEST: 3,
                TicketType.PROBLEM: 2,
                TicketType.CHANGE: 1
            })

        return RandomCollectionNode(TicketType, [], ticket_type_collection)

    def create_ticket_type_queue_node(self, ticket_type_node) -> RandomTableNode:
        random_queue_collection: RandomTable = RandomTableBuilder.build_from_dict(
            TicketType, TicketQueue, {
                TicketType.INCIDENT: {
                    TicketQueue.TECHNICAL_SUPPORT: 40,
                    TicketQueue.CUSTOMER_SERVICE: 10,
                    TicketQueue.BILLING_AND_PAYMENTS: 5,
                    TicketQueue.PRODUCT_SUPPORT: 20,
                    TicketQueue.IT_SUPPORT: 10,
                    TicketQueue.RETURNS_AND_EXCHANGES: 5,
                    TicketQueue.SALES_AND_PRE_SALES: 2,
                    TicketQueue.HUMAN_RESOURCES: 2,
                    TicketQueue.SERVICE_OUTAGES_AND_MAINTENANCE: 5,
                    TicketQueue.GENERAL_INQUIRY: 1
                },
                TicketType.REQUEST: {
                    TicketQueue.TECHNICAL_SUPPORT: 20,
                    TicketQueue.CUSTOMER_SERVICE: 25,
                    TicketQueue.BILLING_AND_PAYMENTS: 15,
                    TicketQueue.PRODUCT_SUPPORT: 15,
                    TicketQueue.IT_SUPPORT: 10,
                    TicketQueue.RETURNS_AND_EXCHANGES: 5,
                    TicketQueue.SALES_AND_PRE_SALES: 5,
                    TicketQueue.HUMAN_RESOURCES: 2,
                    TicketQueue.SERVICE_OUTAGES_AND_MAINTENANCE: 2,
                    TicketQueue.GENERAL_INQUIRY: 1
                },
                TicketType.PROBLEM: {
                    TicketQueue.TECHNICAL_SUPPORT: 30,
                    TicketQueue.CUSTOMER_SERVICE: 15,
                    TicketQueue.BILLING_AND_PAYMENTS: 10,
                    TicketQueue.PRODUCT_SUPPORT: 20,
                    TicketQueue.IT_SUPPORT: 15,
                    TicketQueue.RETURNS_AND_EXCHANGES: 5,
                    TicketQueue.SALES_AND_PRE_SALES: 2,
                    TicketQueue.HUMAN_RESOURCES: 1,
                    TicketQueue.SERVICE_OUTAGES_AND_MAINTENANCE: 1,
                    TicketQueue.GENERAL_INQUIRY: 1
                },
                TicketType.CHANGE: {
                    TicketQueue.TECHNICAL_SUPPORT: 20,
                    TicketQueue.CUSTOMER_SERVICE: 10,
                    TicketQueue.BILLING_AND_PAYMENTS: 5,
                    TicketQueue.PRODUCT_SUPPORT: 20,
                    TicketQueue.IT_SUPPORT: 20,
                    TicketQueue.RETURNS_AND_EXCHANGES: 5,
                    TicketQueue.SALES_AND_PRE_SALES: 5,
                    TicketQueue.HUMAN_RESOURCES: 2,
                    TicketQueue.SERVICE_OUTAGES_AND_MAINTENANCE: 10,
                    TicketQueue.GENERAL_INQUIRY: 3
                }
            }
        )

        return RandomTableNode(TicketType, TicketQueue, [ticket_type_node], random_queue_collection)

    def create_queue_priority_node(self, ticket_type_queue_node):
        random_priority_collection: RandomTable = RandomTableBuilder.build_from_dict(
            TicketQueue, Priority, {
                TicketQueue.TECHNICAL_SUPPORT: {
                    Priority.LOW: 10,
                    Priority.MEDIUM: 30,
                    Priority.HIGH: 60
                },
                TicketQueue.CUSTOMER_SERVICE: {
                    Priority.LOW: 30,
                    Priority.MEDIUM: 50,
                    Priority.HIGH: 20
                },
                TicketQueue.BILLING_AND_PAYMENTS: {
                    Priority.LOW: 20,
                    Priority.MEDIUM: 50,
                    Priority.HIGH: 30
                },
                TicketQueue.PRODUCT_SUPPORT: {
                    Priority.LOW: 20,
                    Priority.MEDIUM: 50,
                    Priority.HIGH: 30
                },
                TicketQueue.IT_SUPPORT: {
                    Priority.LOW: 10,
                    Priority.MEDIUM: 40,
                    Priority.HIGH: 50
                },
                TicketQueue.RETURNS_AND_EXCHANGES: {
                    Priority.LOW: 40,
                    Priority.MEDIUM: 40,
                    Priority.HIGH: 20
                },
                TicketQueue.SALES_AND_PRE_SALES: {
                    Priority.LOW: 30,
                    Priority.MEDIUM: 50,
                    Priority.HIGH: 20
                },
                TicketQueue.HUMAN_RESOURCES: {
                    Priority.LOW: 50,
                    Priority.MEDIUM: 40,
                    Priority.HIGH: 10
                },
                TicketQueue.SERVICE_OUTAGES_AND_MAINTENANCE: {
                    Priority.LOW: 10,
                    Priority.MEDIUM: 20,
                    Priority.HIGH: 70
                },
                TicketQueue.GENERAL_INQUIRY: {
                    Priority.LOW: 60,
                    Priority.MEDIUM: 30,
                    Priority.HIGH: 10
                }
            }
        )

        return RandomTableNode(TicketQueue, Priority, [ticket_type_queue_node], random_priority_collection)

    def create_language_node(self) -> RandomCollectionNode:
        random_language_collection: IRandom = RandomCollectionBuilder.build_from_value_weight_dict(
            { Language.DE: 2, Language.EN: 4, Language.FR: 1, Language.ES: 2 })

        return RandomCollectionNode(Language, [], random_language_collection)
