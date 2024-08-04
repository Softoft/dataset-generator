import random
from dataclasses import dataclass
from enum import Enum
from random import choices

from synthetic_data_generator.random_generators.random_collection_interface import IRandom


@dataclass
class RandomCollection[V](IRandom):
    values: list[V]
    weights: list[float]
    randomization_factor: float = 1.5

    def __post_init__(self):
        self._randomize_weights()

    def get_random_value(self, excluding: list = None) -> V:
        excluding = excluding or []
        result = choices(self.values, weights=self.weights)[0]
        while result in excluding:
            result = choices(self.values, weights=self.weights)[0]
        return result

    def _get_random_value_between(self, min_value: float, max_value: float) -> float:
        return min_value + (max_value - min_value) * random.random()

    def _randomize_weights(self):
        self.weights = [
            weight * self._get_random_value_between(1, 1 * self.randomization_factor)
            for weight in self.weights]


class RandomCollectionFactory:
    def build_from_enum(self, enum_type: type[Enum]):
        return RandomCollection[enum_type](list(enum_type), [1 for _ in range(len(enum_type))])

    def build_from_value_weight_dict[V](self, value_weight_dict: dict[V, float]):
        return RandomCollection[V](list(value_weight_dict.keys()), list(value_weight_dict.values()))

    def build_from_list_of_values[V](self, values: list[V]):
        return RandomCollection[V](values, [1 for _ in range(len(values))])
