from dataclasses import dataclass
from typing import Optional

from graph.data.category_ticket_field import CategoricalTicketField, InputTicketField


class Language(CategoricalTicketField):
    DE = "Deutsch", "Schreibe auf deutsch"
    EN = "Englisch", "Schreibe in englisch."
    FR = "Französisch", "Schreibe in französisch."
    ES = "Spanisch", "Schreibe in spanisch."
    PT = "Portugiesisch", "Schreibe in portugiesisch."


class Priority(CategoricalTicketField):
    LOW = 1, "Low priority, ticket concerns less urgent matters, not requiring immediate attention."
    MEDIUM = 2, "Medium priority, ticket concerns important matters, should be addressed promptly but not critical."
    HIGH = 3, "High priority, ticket concerns urgent matters, requiring immediate attention and quick resolution."



@dataclass
class TicketEmail:
    subject: str
    body: str


@dataclass
class TicketExtraInformation:
    topic: str
    product_category: str
    product: str


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


@dataclass
class TicketTextLength(InputTicketField):
    lower_bound: int
    upper_bound: int

    def get_description(self):
        return f"Die Länge des Textes liegt zwischen {self.lower_bound} und {self.upper_bound} Zeichen."

    def __eq__(self, other):
        return self.lower_bound == other.lower_bound and self.upper_bound == other.upper_bound

    def __hash__(self):
        return hash((self.lower_bound, self.upper_bound))


class TicketType(CategoricalTicketField):
    INCIDENT = "Incident", "Unexpected issue, immediate attention needed."
    REQUEST = "Request", "Routine inquiry or request."
    PROBLEM = "Problem", "Basic issue, causing multiple incidents."
    CHANGE = "Change", "Planned change or update."


@dataclass
class Ticket:
    subject: str
    body: str
    answer: str
    type: TicketType
    queue: TicketQueue
    priority: Priority
    language: Optional[Language] = None
