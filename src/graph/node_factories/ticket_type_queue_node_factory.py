from graph.nodes.core.executable_node import INode
from graph.nodes.core.random_table_node import RandomTableNode
from graph.data.models import TicketQueue, TicketType
from random_collections.random_collection_table import RandomTable, RandomTableBuilder


def create_ticket_type_queue_node(ticket_type_node: INode) -> RandomTableNode:
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
