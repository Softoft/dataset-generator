from dataclasses import dataclass
from typing import Optional

from graph.data.ticket_field import CategoricalTicketField, ComparableEnum, InputTicketField


class Language(ComparableEnum):
    DE = "German"
    EN = "English"
    FR = "French"
    ES = "Spanish"
    PT = "Portuguese"


class Priority(CategoricalTicketField):
    LOW = "low", "Low priority, ticket concerns less urgent matters, not requiring immediate attention."
    MEDIUM = "medium", "Medium priority, ticket concerns important matters, should be addressed promptly but not critical."
    HIGH = "high", "High priority, ticket concerns urgent matters, requiring immediate attention and quick resolution."


@dataclass
class TicketEmail:
    subject: str
    body: str


@dataclass
class TicketExtraInformation:
    ticket_categories: list[str]
    business_type: str
    product_category: str
    product_sub_category: str
    product: str
    version: str
    extra_info: str


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
    language: Language
    business_type: str
    product_category: str
    product_sub_category: str
    product: str
    version: str

    tags: Optional[list[str]] = None

    def __repr__(self):
        return f"TranslatedTicket(subject={self.subject},\nbody={self.body},\nanswer={self.answer},\ntype={self.type},\nqueue={self.queue},\npriority={self.priority},\nlanguage={self.language})"

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self

    def to_dict(self):
        return {
            "subject": self.subject,
            "body": self.body,
            "answer": self.answer,
            "type": self.type.value,
            "queue": self.queue.value,
            "priority": self.priority.value,
            "language": self.language.value,
            "business_type": self.business_type,
            "product_category": self.product_category,
            "product_sub_category": self.product_sub_category,
            "product": self.product,
            "version": self.version,
            "tags": self.tags or []
        }
