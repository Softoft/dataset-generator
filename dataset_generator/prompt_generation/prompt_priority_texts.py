from dataset_generator.ticket_fields.priority import Priority


def get_priorities_prompt(priority: Priority)-> str:
    match priority:
        case Priority.LOW:
            return """
Die Priorität ist niedrig, das bedeutet:
Das Ticket ist unwichtig, es besteht wenig Zeitdruck:
Es ist ein kleiner Fehler in der verwendeten Software oder Hardware aufgefallen.
Frage ob seine nächste Rechnung, einen anderen Unternehmensname angeben kann.
Frage ob er ein Angebot haben kann, aber er hat es nicht eilig oder braucht es nicht wirklich.
Ein Kunde gibt positives Feedback, ohne konkreten Handlungsbedarf
Kunde schreibt, dass er für sein System vielleicht ein Update gebrauchen könnte.
Kunde fragt, ob er für eine Rechnung eine kleine Änderung bekommen kann"""

        case Priority.MEDIUM:
            return """
Die Priorität ist mittel/normal, das bedeutet:
sind normale Standard Probleme, die nicht direkt erledigt werden müssen und keinen starken Effekt haben.
Kunde braucht Update auf neue Software Version. Dem Kunden ist ein Bug aufgefallen. Sein Gerät hat einen kleinen Fehler.
Braucht eine Rechnung. Neuer Kunde will ein Angebot für eine Software Entwicklung haben.
Ein bestehender Kunde hat sich beschwert, dass seine Emails nicht beantwortet wurde.Kunde hat sich beschwert."""

        case Priority.HIGH:
            return """
Die Priorität ist hoch, das bedeutet:
Wenn jemand gehackt wurde, sein Gerät sich nicht einschalten lässt, er das Gerät/Software aber braucht.
Wenn er das Gerät/Software nicht verwenden kann, aus unterschiedlichen Gründen, er es aber braucht.
Wenn jemand unbedingt eine Rechnung benötigt, aus verschiedenen Gründen,
Falls ein Kunde ein Security Update, gegen eine ernstzunehmende Sicherheitslücke gefunden hat.
            """
        case _:
            raise ValueError("Invalid Priority")