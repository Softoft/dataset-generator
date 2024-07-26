from graph.node_factories.language_node_factory import create_language_node
from graph.node_factories.text_length_node_factory import create_text_length_node
from graph.node_factories.ticket_queue_priority_node import create_queue_priority_node
from graph.node_factories.ticket_type_node_factory import create_ticket_type_node
from graph.node_factories.ticket_type_queue_node_factory import create_ticket_type_queue_node
from graph.nodes.ticket_email_node import TicketEmailNode
from graph.nodes.ticket_extra_information_node import TicketExtraInformationNode


class Graph:
    def __init__(self, ticket_text_length_mean=250, ticket_text_length_standard_deviation=400):
        self.ticket_type_node = create_ticket_type_node()
        self.ticket_queue_node = create_ticket_type_queue_node(self.ticket_type_node)
        self.ticket_queue_priority_node = create_queue_priority_node(self.ticket_queue_node)
        self.language_node = create_language_node()
        self.text_length_node = create_text_length_node(mean=ticket_text_length_mean, standard_deviation=ticket_text_length_standard_deviation)
        self.ticket_extra_information_node = TicketExtraInformationNode([self.ticket_type_node, self.ticket_queue_node])
        self.ticket_email_generator_node = TicketEmailNode([self.ticket_extra_information_node, self.ticket_queue_priority_node, self.language_node, self.text_length_node])
