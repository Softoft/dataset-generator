import random
from random import choices


class IRandomCollection[T]:
    def get_random_value(self, *args, **kwargs) -> T:
        pass


class RandomCollection[T](IRandomCollection):
    @classmethod
    def from_value_list(cls, values: list[T]) -> IRandomCollection[T]:
        return cls(value_weight_dict={value: 1 for value in values})

    def __init__(self, value_weight_dict: dict[T, float]):
        self.value_weight_dict = value_weight_dict
        self._randomize_weights()

    def _randomize_weights(self):
        for key in self.value_weight_dict.keys():
            self.value_weight_dict[key] *= random.random()

    def get_random_value(self) -> T:
        values, weights = zip(*self.value_weight_dict.items())
        return choices(values, weights=weights)[0]