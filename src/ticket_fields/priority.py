from src.random_collections.random_collection_interface import IRandom
from src.random_collections.random_collection_table import RandomTableBuilder
from src.ticket_fields.category_ticket_field import CategoricalTicketField
from src.ticket_fields.queue import TicketQueue


class Priority(CategoricalTicketField):
    LOW = 1, "Niedrige Priorität, das Ticket betrifft weniger dringende Angelegenheiten, die nicht sofortige Aufmerksamkeit erfordern."
    MEDIUM = 2, "Mittlere Priorität, das Ticket betrifft wichtige Angelegenheiten, die zeitnah behandelt werden sollten, aber nicht kritisch sind."
    HIGH = 3, "Hohe Priorität, das Ticket betrifft dringende Angelegenheiten, die sofortige Aufmerksamkeit und schnelle Lösung erfordern."


random_priority_collection: IRandom = RandomTableBuilder.build_from_dict(
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
