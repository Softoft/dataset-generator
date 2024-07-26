from graph.data.category_ticket_field import CategoricalTicketField


class TicketType(CategoricalTicketField):
    INCIDENT = "Incident", "Unexpected issue, immediate attention needed."
    REQUEST = "Request", "Routine inquiry or request."
    PROBLEM = "Problem", "Basic issue, causing multiple incidents."
    CHANGE = "Change", "Planned change or update."
