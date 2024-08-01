import dataclasses
import math

import numpy as np

from graph.data.models import NumberInterval


@dataclasses.dataclass
class NumberIntervalGenerator:
    """
    Generates a random number interval based on a normal distribution.
    mean: int
    standard_deviation: int
    min_upper_bound_difference: int = 2
    lower_number_min_value: int = 0
    lower_number_max_value: int = 10 ** 12
    """
    mean: int
    standard_deviation: int
    min_upper_bound_difference: int = 2
    lower_number_min_value: int = 0
    lower_number_max_value: int = 10 ** 12

    def __post_init__(self):
        assert self._is_in_bound(self.mean), "Mean is out of bounds"
        assert self.min_upper_bound_difference > 1

    def _is_in_bound(self, number: float | int) -> bool:
        return self.lower_number_min_value < number < self.lower_number_max_value

    def _generate_random_normal_distribution_number(self) -> int:
        return round(np.random.normal(self.mean, self.standard_deviation))

    def _generate_bounded_number(self) -> int:
        text_length = self._generate_random_normal_distribution_number()
        while not self._is_in_bound(text_length):
            text_length = self._generate_random_normal_distribution_number()
        return text_length

    def _generate_upper_bound(self, text_length: int) -> int:
        upper_bound_factor = math.log2(abs(text_length) + self.min_upper_bound_difference)
        return round(text_length + self.min_upper_bound_difference * upper_bound_factor)

    def generate_bounds(self) -> NumberInterval:
        text_length = self._generate_bounded_number()
        return NumberInterval(lower_bound=text_length, upper_bound=self._generate_upper_bound(text_length))
