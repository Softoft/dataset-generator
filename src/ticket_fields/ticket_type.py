from src.random_collections.random_collection import RandomCollectionBuilder
from src.ticket_fields.category_ticket_field import CategoricalTicketField


class TicketType(CategoricalTicketField):
    INCIDENT = "Incident", "Unerwartetes Problem, sofortige Aufmerksamkeit nötig."
    REQUEST = "Request", "Routineanfrage oder -anforderung."
    PROBLEM = "Problem", "Grundlegendes Problem, verursacht mehrere Vorfälle."
    CHANGE = "Change", "Geplante Änderung oder Update."


ticket_type_collection = RandomCollectionBuilder.build_from_value_weight_dict(
    {
        TicketType.INCIDENT: 4,
        TicketType.REQUEST: 3,
        TicketType.PROBLEM: 2,
        TicketType.CHANGE: 1
    })
