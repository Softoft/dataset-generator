from graph.data.category_ticket_field import CategoricalTicketField


class Priority(CategoricalTicketField):
    LOW = 1, "Low priority, ticket concerns less urgent matters, not requiring immediate attention."
    MEDIUM = 2, "Medium priority, ticket concerns important matters, should be addressed promptly but not critical."
    HIGH = 3, "High priority, ticket concerns urgent matters, requiring immediate attention and quick resolution."
