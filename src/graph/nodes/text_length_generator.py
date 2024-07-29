import dataclasses
import math

import numpy as np

from graph.data.models import TicketTextLength


@dataclasses.dataclass
class NumberIntervalGenerator:
    mean: int
    standard_deviation: int
    lower_number_min_value: int = 30
    lower_number_max_value: int = 1000
    min_upper_bound_difference: int = 20

    def __post_init__(self):
        assert self._is_in_bound(self.mean), "Mean is out of bounds"

    def _is_in_bound(self, number: float | int) -> bool:
        return self.lower_number_min_value < number < self.lower_number_max_value

    def _generate_random_normal_distribution_text_length(self) -> int:
        return int(np.random.normal(self.mean, self.standard_deviation))

    def _generate_bounded_text_length(self) -> int:
        text_length = self._generate_random_normal_distribution_text_length()
        while not self._is_in_bound(text_length):
            text_length = self._generate_random_normal_distribution_text_length()
        return text_length

    def _generate_upper_text_length(self, text_length: int) -> int:
        upper_bound_factor = math.log(10 + abs(text_length), 10)
        return int(text_length + self.min_upper_bound_difference * upper_bound_factor)

    def generate_text_length_bounds(self) -> TicketTextLength:
        text_length = self._generate_bounded_text_length()
        return TicketTextLength(lower_bound=text_length, upper_bound=self._generate_upper_text_length(text_length))
