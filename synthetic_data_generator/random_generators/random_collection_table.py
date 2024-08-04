from enum import Enum

from synthetic_data_generator.random_generators.random_collection import RandomCollection,\
    RandomCollectionFactory
from synthetic_data_generator.random_generators.random_collection_interface import IRandom


class RandomTable[K: Enum, V: Enum](IRandom):
    def __init__(self, value_weight_dict: dict[K, RandomCollection[V]]):
        self.value_weight_dict = value_weight_dict

    def get_random_value(self, key: K) -> V:
        return self.value_weight_dict[key].get_random_value()


class RandomTableBuilder:
    def build_from_weight_table(self, key_enum: type[Enum], value_enum: type[Enum], weights: list[list[float]]):
        return RandomTable(
            { key: RandomCollection(list(value_enum), weights) for key, weights in zip(list(key_enum), weights) })

    def validate_value_weight_dict[K, V](self, key_enum: type[K], value_enum: type[V],
                                         value_weight_dict: dict[K, dict[V, float]]):
        assert set(key_enum) == set(value_weight_dict.keys()), "Keys in value_weight_dict must match key_enum"
        for key in list(key_enum):
            assert set(value_enum) == set(
                value_weight_dict[key].keys()), "Values in value_weight_dict must match value_enum"

    def build_from_dict[K, V](self, key_enum: type[K], value_enum: type[V], value_weight_dict: dict[K, dict[V, float]]):
        RandomTableBuilder().validate_value_weight_dict(key_enum, value_enum, value_weight_dict)
        return RandomTable(
            { key: RandomCollectionFactory().build_from_value_weight_dict(value_weight_dict[key]) for key in
              list(key_enum) })
