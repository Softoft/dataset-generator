from graph.data.category_ticket_field import CategoricalTicketField


class TicketType(CategoricalTicketField):
    INCIDENT = "Incident", "Unerwartetes Problem, sofortige Aufmerksamkeit nötig."
    REQUEST = "Request", "Routineanfrage oder -anforderung."
    PROBLEM = "Problem", "Grundlegendes Problem, verursacht mehrere Vorfälle."
    CHANGE = "Change", "Geplante Änderung oder Update."
