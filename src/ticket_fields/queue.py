from src.ticket_fields.random_collection import IRandom, RandomTableBuilder

from src.ticket_fields.category_ticket_field import CategoricalTicketField
from src.ticket_fields.ticket_type import TicketType


class TicketQueue(CategoricalTicketField):
    TECHNICAL_SUPPORT = "Technical Support", "Technische Probleme und Supportanfragen."
    CUSTOMER_SERVICE = "Customer Service", "Kundenanfragen und Serviceanfragen."
    BILLING_AND_PAYMENTS = "Billing and Payments", "Abrechnungsprobleme und Zahlungsabwicklung."
    PRODUCT_SUPPORT = "Product Support", "Support für produktbezogene Probleme."
    IT_SUPPORT = "IT Support", "Interner IT-Support und Infrastrukturprobleme."
    RETURNS_AND_EXCHANGES = "Returns and Exchanges", "Produktrückgaben und -umtausch."
    SALES_AND_PRE_SALES = "Sales and Pre-Sales", "Verkaufsanfragen und Pre-Sales-Fragen."
    HUMAN_RESOURCES = "Human Resources", "Mitarbeiteranfragen und HR-bezogene Probleme."
    SERVICE_OUTAGES_AND_MAINTENANCE = "Service Outages and Maintenance", "Dienstunterbrechungen und Wartung."
    GENERAL_INQUIRY = "General Inquiry", "Allgemeine Anfragen und Informationsanfragen."


random_queue_collection: IRandom = RandomTableBuilder.build_from_dict(
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
