from graph.data.priority import Priority
from graph.data.ticket_queue import TicketQueue
from graph.data.ticket_text_length import TicketTextLength
from graph.data.ticket_type import TicketType


class PromptGenerator:
    def create_prompt(self, ticket_type: TicketType, ticket_queue: TicketQueue, priority: Priority,
                      ticket_text_length: TicketTextLength):
        return (
            f"Generate email text and subject. For a ticket, with type {ticket_type.value}: {ticket_type.description},"
            f"for the queue {ticket_queue.value}: {ticket_queue.description},"
            f"for the priority {priority.value}: {priority.description},"
            f"The text needs to have between  {ticket_text_length.lower_bound} and {ticket_text_length.upper_bound} characters")
