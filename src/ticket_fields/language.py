from enum import Enum

from src.random_collections.random_collection import RandomCollectionBuilder
from src.random_collections.random_collection_interface import IRandom


class Language(Enum):
    DE = "Deutsch"
    EN = "Englisch"
    FR = "Französisch"
    ES = "Spanisch"
    PT = "Portugiesisch"


random_language_collection: IRandom = RandomCollectionBuilder.build_from_value_weight_dict(
    {Language.DE: 2, Language.EN: 4, Language.FR: 1, Language.ES: 2})
