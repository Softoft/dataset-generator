import enum

from dataset_generator.ticket_fields.random_collection import IRandomCollection, RandomCollection


class Language(enum.Enum):
    DE = "Deutsch"
    EN = "Englisch"
    FR = "Französisch"
    ES = "Spanisch"


random_language_collection: IRandomCollection = RandomCollection(
    {Language.DE: 2, Language.EN: 4, Language.FR: 1, Language.ES: 2})
