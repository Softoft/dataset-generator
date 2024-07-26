from graph.data.category_ticket_field import CategoricalTicketField


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
