from enum import Enum

from src.random_collections.random_collection import RandomCollection, RandomCollectionBuilder
from src.random_collections.random_collection_interface import IRandom


class RandomTable[K: Enum, V: Enum](IRandom):
    def __init__(self, value_weight_dict: dict[K, RandomCollection[V]]):
        self.value_weight_dict = value_weight_dict

    def get_random_value(self, key: K) -> V:
        return self.value_weight_dict[key].get_random_value()


class RandomTableBuilder:
    @staticmethod
    def build_from_weight_table(key_enum: type[Enum], value_enum: type[Enum], weights: list[list[float]]):
        return RandomTable(
            { key: RandomCollection(list(value_enum), weights) for key, weights in zip(list(key_enum), weights) })

    @staticmethod
    def validate_value_weight_dict[K: Enum, V: Enum](key_enum: type[K], value_enum: type[V],
                                                     value_weight_dict: dict[K, dict[V, float]]):
        assert set(key_enum) == set(value_weight_dict.keys()), "Keys in value_weight_dict must match key_enum"
        for key in list(key_enum):
            assert set(value_enum) == set(value_weight_dict[key].keys()), "Values in value_weight_dict must match value_enum"

    @staticmethod
    def build_from_dict[K: Enum, V: Enum](key_enum: type[K], value_enum: type[V],
                                          value_weight_dict: dict[K, dict[V, float]]):
        # RandomTableBuilder.validate_value_weight_dict(key_enum, value_enum, value_weight_dict)
        return RandomTable(
            { key: RandomCollectionBuilder.build_from_value_weight_dict(value_weight_dict[key]) for key in
              list(key_enum) })
