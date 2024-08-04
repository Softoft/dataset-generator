from graph.nodes.core.executable_node import INode
from graph.nodes.core.random_table_node import RandomTableNode
from synthetic_data_generator.ai_graph.data.models import Priority, TicketQueue

from synthetic_data_generator.random_generators.random_collection_table import RandomTable,\
    RandomTableBuilder


def create_queue_priority_node(ticket_type_queue_node: INode):
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
