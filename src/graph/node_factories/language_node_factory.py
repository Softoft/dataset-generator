from graph.nodes.random_collection_node import RandomCollectionNode
from graph.data.language import Language
from random_collections.random_collection import RandomCollectionBuilder
from random_collections.random_collection_interface import IRandom


def create_language_node() -> RandomCollectionNode:
    random_language_collection: IRandom = RandomCollectionBuilder.build_from_value_weight_dict(
        { Language.DE: 2, Language.EN: 4, Language.FR: 1, Language.ES: 2 })

    return RandomCollectionNode(Language, [], random_language_collection)
