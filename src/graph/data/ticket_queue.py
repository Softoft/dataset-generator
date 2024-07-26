from graph.data.category_ticket_field import CategoricalTicketField


class TicketQueue(CategoricalTicketField):
    TECHNICAL_SUPPORT = "Technical Support", "Technical issues and support requests."
    CUSTOMER_SERVICE = "Customer Service", "Customer inquiries and service requests."
    BILLING_AND_PAYMENTS = "Billing and Payments", "Billing issues and payment processing."
    PRODUCT_SUPPORT = "Product Support", "Support for product-related issues."
    IT_SUPPORT = "IT Support", "Internal IT support and infrastructure issues."
    RETURNS_AND_EXCHANGES = "Returns and Exchanges", "Product returns and exchanges."
    SALES_AND_PRE_SALES = "Sales and Pre-Sales", "Sales inquiries and pre-sales questions."
    HUMAN_RESOURCES = "Human Resources", "Employee inquiries and HR-related issues."
    SERVICE_OUTAGES_AND_MAINTENANCE = "Service Outages and Maintenance", "Service interruptions and maintenance."
    GENERAL_INQUIRY = "General Inquiry", "General inquiries and information requests."
