from graph.data.category_ticket_field import CategoricalTicketField


class Priority(CategoricalTicketField):
    LOW = 1, "Niedrige Priorität, das Ticket betrifft weniger dringende Angelegenheiten, die nicht sofortige Aufmerksamkeit erfordern."
    MEDIUM = 2, "Mittlere Priorität, das Ticket betrifft wichtige Angelegenheiten, die zeitnah behandelt werden sollten, aber nicht kritisch sind."
    HIGH = 3, "Hohe Priorität, das Ticket betrifft dringende Angelegenheiten, die sofortige Aufmerksamkeit und schnelle Lösung erfordern."
