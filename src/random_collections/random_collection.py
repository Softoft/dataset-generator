import random
from enum import Enum
from random import choices

from src.random_collections.random_collection_interface import IRandom


class RandomCollection[V: Enum](IRandom):
    def __init__(self, values: list[V], weights: list[float], randomization_factor: float = 1.5):
        self.randomization_factor = randomization_factor
        self._values = values
        self._weights = weights
        self._randomize_weights()

    def get_random_value(self, excluding: list = None) -> V:
        excluding = excluding or []
        result = choices(self._values, weights=self._weights)[0]
        while result in excluding:
            result = choices(self._values, weights=self._weights)[0]
        return result

    def _get_random_value_between(self, min_value: float, max_value: float) -> float:
        return min_value + (max_value - min_value) * random.random()

    def _randomize_weights(self):
        self._weights = [
            weight * self._get_random_value_between(1, 1 * self.randomization_factor)
            for weight in self._weights]


class RandomCollectionBuilder:
    @staticmethod
    def build_from_enum(enum_type: type[Enum]):
        return RandomCollection[enum_type](list(enum_type), [1 for _ in range(len(enum_type))])

    @staticmethod
    def build_from_value_weight_dict[V](value_weight_dict: dict[V, float]):
        return RandomCollection[V](list(value_weight_dict.keys()), list(value_weight_dict.values()))


