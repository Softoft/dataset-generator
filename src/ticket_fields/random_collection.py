import enum
import random
from random import choices


class IRandomCollection[V: enum.Enum]:
    def get_random_value(self, *args, **kwargs) -> V:
        pass


class RandomCollection[V: enum.Enum](IRandomCollection):
    def __init__(self, values: list[V], weights: list[float]):
        self._percent_randomizer = 0.1
        self._values = values
        self._weights = weights
        self._randomize_weights()

    def _get_random_value_between(self, min_value: float, max_value: float) -> float:
        return min_value + (max_value - min_value) * random.random()

    def _randomize_weights(self):
        self._weights = [
            weight * self._get_random_value_between(1 - self._percent_randomizer, 1 + self._percent_randomizer)
            for weight in self._weights]

    def get_random_value(self) -> V:
        return choices(self._values, weights=self._weights)[0]


class RandomCollectionBuilder:
    def __init__(self):
        self.values = []
        self.weights = []

    def __add_value(self, value, weight):
        self.values.append(value)
        self.weights.append(weight)

    def from_enum(self, enum_type: type[enum.Enum]):
        return RandomCollection[enum_type](list(enum_type), [1 for _ in range(len(enum_type))])

    def build_from_value_weight_dict[V](self, value_weight_dict: dict[V, float]):
        for value, weight in value_weight_dict.items():
            self.__add_value(value, weight)
        return RandomCollection[V](self.values, self.weights)


class RandomTable[K: enum.Enum, V: enum.Enum](IRandomCollection):
    def __init__(self, value_weight_dict: dict[K, RandomCollection[V]]):
        self.value_weight_dict = value_weight_dict

    def get_random_value(self, key: K) -> V:
        return self.value_weight_dict[key].get_random_value()


class RandomTableBuilder[K: enum.Enum, V: enum.Enum]:
    def __init__(self):
        self._value_weight_dict: dict[K, RandomCollection[V]] = {}

    def add_value_weight_2d(self, key_enum: type[K], value_enum: type[V], weights: list[list[float]]):
        keys = list(key_enum)
        values = list(value_enum)
        for key, weight_list in zip(keys, weights):
            self._value_weight_dict[key] = RandomCollection(values, weight_list)

    def build(self) -> RandomTable[K, V]:
        return RandomTable(self._value_weight_dict)
