from graph.node_factories.language_node_factory import create_language_node
from graph.node_factories.text_length_node_factory import create_text_length_node
from graph.node_factories.ticket_queue_priority_node import create_queue_priority_node
from graph.node_factories.ticket_type_node_factory import create_ticket_type_node
from graph.node_factories.ticket_type_queue_node_factory import create_ticket_type_queue_node


class Graph:
    def __init__(self, ticket_text_length_mean=200, ticket_text_length_standard_deviation=200):
        self.ticket_type_node = create_ticket_type_node()
        self.ticket_queue_node = create_ticket_type_queue_node(self.ticket_type_node)
        self.ticket_queue_priority_node = create_queue_priority_node(self.ticket_queue_node)
        self.language_node = create_language_node()
        self.text_length_node = create_text_length_node(mean=ticket_text_length_mean, standard_deviation=ticket_text_length_standard_deviation)
