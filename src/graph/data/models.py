import dataclasses
import random
from dataclasses import dataclass
from typing import Optional

from graph.data.ticket_field import ComparableEnum, InputTicketField, OutputDataclassField,\
    RandomTicketField


class Language(ComparableEnum):
    DE = "German"
    EN = "English"
    FR = "French"
    ES = "Spanish"
    PT = "Portuguese"

    @property
    def iso_upper(self):
        return self.name

    @property
    def iso_lower(self):
        return self.name.lower()

    @property
    def english_name(self):
        return self.value


class Priority(RandomTicketField):
    LOW = ("low", [
        "Ticket concerns less urgent matters.",
        "This ticket_a does not require immediate attention.",
        "Low priority: issue is not time-sensitive.",
        "Non-urgent ticket_a.",
        "This ticket_a can be addressed at a later time.",
        "The issue is of low priority.",
        "Not requiring immediate resolution."
    ])
    MEDIUM = ("medium", [
        "Medium priority: ticket_a concerns important matters.",
        "Should be addressed promptly but not critical.",
        "Ticket requires timely attention.",
        "Important but not urgent issue.",
        "Moderate priority: handle as soon as possible.",
        "Ticket is of medium importance.",
        "Needs prompt but not immediate action."
    ])
    HIGH = ("high", [
        "High priority: ticket_a concerns urgent matters.",
        "Requiring immediate attention and quick resolution.",
        "Critical issue: needs immediate action.",
        "Urgent matter: resolve as soon as possible.",
        "Top priority: address immediately.",
        "High importance: requires fast resolution.",
        "Immediate attention needed for this ticket_a."
    ])


@dataclass
class TicketEmail(InputTicketField):
    subject: str
    body: str

    def get_description(self):
        return f"Email: subject:'{self.subject}'; body'{self.body}'."


@dataclass
class TicketExtraInformation(OutputDataclassField):
    business_type: str
    product: str
    extra_info: str

    def __post_init__(self):
        assert len(self.business_type) < 60, "Business type must be less than 60 characters."
        assert len(self.product) < 60, "Product must be less than 60 characters."
        assert 10 < len(self.extra_info) < 200, "Extra info must be between 10 and 200 characters."

    def to_dict(self):
        return dataclasses.asdict(self)


class TicketQueue(RandomTicketField):
    TECHNICAL_SUPPORT = ("Technical Support", [
        "Technical issues and support requests.",
        "Help with technical problems.",
        "Support for technical difficulties.",
        "Assistance with technology-related issues.",
        "Technical troubleshooting and support.",
        "Resolving technical problems.",
        "Handling technical queries and issues."
    ])
    CUSTOMER_SERVICE = ("Customer Service", [
        "Customer inquiries and service requests.",
        "Assistance with customer-related issues.",
        "Handling customer service queries.",
        "Support for customer-related matters.",
        "Customer care and support.",
        "Addressing customer questions.",
        "Providing service to customers."
    ])
    BILLING_AND_PAYMENTS = ("Billing and Payments", [
        "Billing issues and payment processing.",
        "Help with billing and payments.",
        "Resolving payment-related issues.",
        "Support for billing queries.",
        "Assistance with payment problems.",
        "Handling billing concerns.",
        "Processing payment issues."
    ])
    PRODUCT_SUPPORT = ("Product Support", [
        "Support for product-related issues.",
        "Assistance with product problems.",
        "Resolving product-related queries.",
        "Help with product concerns.",
        "Support for issues related to products.",
        "Handling product support requests.",
        "Providing support for product issues."
    ])
    IT_SUPPORT = ("IT Support", [
        "Internal IT support and infrastructure issues.",
        "Assistance with IT-related problems.",
        "Support for IT infrastructure.",
        "Handling internal IT queries.",
        "Resolving IT support requests.",
        "Help with IT systems and infrastructure.",
        "Providing IT support."
    ])
    RETURNS_AND_EXCHANGES = ("Returns and Exchanges", [
        "Product returns and exchanges.",
        "Assistance with returning products.",
        "Handling product exchanges.",
        "Support for returns and exchanges.",
        "Help with product return issues.",
        "Processing exchanges and returns.",
        "Providing support for returns and exchanges."
    ])
    SALES_AND_PRE_SALES = ("Sales and Pre-Sales", [
        "Sales inquiries and pre-sales questions.",
        "Assistance with sales-related queries.",
        "Handling pre-sales questions.",
        "Support for sales inquiries.",
        "Help with pre-sales information.",
        "Providing sales support.",
        "Addressing sales and pre-sales concerns."
    ])
    HUMAN_RESOURCES = ("Human Resources", [
        "Employee inquiries and HR-related issues.",
        "Assistance with HR matters.",
        "Handling employee-related queries.",
        "Support for HR issues.",
        "Help with human resources concerns.",
        "Addressing employee inquiries.",
        "Providing HR support."
    ])
    SERVICE_OUTAGES_AND_MAINTENANCE = ("Service Outages and Maintenance", [
        "Service interruptions and maintenance.",
        "Assistance with service outages.",
        "Handling maintenance-related issues.",
        "Support for service interruptions.",
        "Help with maintenance queries.",
        "Resolving service outages.",
        "Providing support for maintenance issues."
    ])
    GENERAL_INQUIRY = ("General Inquiry", [
        "General inquiries and information requests.",
        "Assistance with general questions.",
        "Handling information requests.",
        "Support for general queries.",
        "Help with general information.",
        "Addressing general inquiries.",
        "Providing support for general questions."
    ])


@dataclass
class NumberInterval:
    lower_bound: float
    upper_bound: float

    def __contains__(self, item: float | int):
        return self.lower_bound <= item <= self.upper_bound

    def __eq__(self, other):
        return self.lower_bound == other.lower_bound and self.upper_bound == other.upper_bound

    def __hash__(self):
        return hash((self.lower_bound, self.upper_bound))


class TicketType(RandomTicketField):
    INCIDENT = ("Incident", [
        "Unexpected issue, immediate attention needed.",
        "Urgent problem requiring prompt action.",
        "Unplanned event needing immediate resolution.",
        "Critical issue requiring swift attention.",
        "Unexpected problem, high urgency.",
        "Immediate action required for incident.",
        "Urgent incident that needs quick response."
    ])
    REQUEST = ("Request", [
        "Routine inquiry or request.",
        "Standard request needing attention.",
        "Normal service request.",
        "General inquiry or request.",
        "Routine question or request for information.",
        "Non-urgent request for service.",
        "Regular request requiring handling."
    ])
    PROBLEM = ("Problem", [
        "Basic issue, causing multiple incidents.",
        "Underlying problem leading to other issues.",
        "Core issue affecting multiple areas.",
        "Problem causing several incidents.",
        "Root cause of various incidents.",
        "Major issue leading to other problems.",
        "Primary issue causing multiple incidents."
    ])
    CHANGE = ("Change", [
        "Planned change or update.",
        "Scheduled change needing implementation.",
        "Planned update or modification.",
        "Change request for approval and action.",
        "Planned modification requiring execution.",
        "Scheduled update to be carried out.",
        "Change implementation request."
    ])


class UniqueIDGenerator:
    def __init__(self):
        self.used_ids = set()
        self.max_id = 100_000

    def generate_id(self):
        if len(self.used_ids) >= self.max_id:
            raise Exception("No more unique IDs available.")

        while True:
            new_id = random.randint(1, self.max_id)
            if new_id not in self.used_ids:
                self.used_ids.add(new_id)
                return new_id


id_generator = UniqueIDGenerator()


@dataclass
class Ticket:
    subject: str
    body: str
    answer: str
    type: TicketType
    queue: TicketQueue
    priority: Priority
    language: Language
    ticket_extra_information: TicketExtraInformation
    tags: Optional[list[str]] = None

    def __repr__(self):
        return f"TranslatedTicket(subject={self.subject},\nbody={self.body},\nanswer={self.answer},\ntype={self.type},\nqueue={self.queue},\npriority={self.priority},\nlanguage={self.language})"

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self

    def to_dict(self):
        result = {
            "id": id_generator.generate_id(),
            "subject": self.subject,
            "body": self.body,
            "answer": self.answer,
            "type": self.type.value,
            "queue": self.queue.value,
            "priority": self.priority.value,
            "language": self.language.iso_lower,
            "tags": self.tags or []
        }

        extra_info = self.ticket_extra_information.to_dict()

        result.update(extra_info)
        return result
