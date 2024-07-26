import dataclasses
import math

import numpy as np

from graph.data.ticket_text_length import TicketTextLength

rng = np.random.default_rng(seed=42)


@dataclasses.dataclass
class TextLengthGenerator:
    mean: int
    standard_deviation: int
    _lower_text_length_min_value: int = 30
    _min_upper_bound_difference: int = 20

    def __post_init__(self):
        assert self._is_in_bound(self.mean), "Mean is out of bounds"
        assert self._lower_text_length_min_value >= 0, "Lower bound is negative"

    def _is_in_bound(self, number: float | int) -> bool:
        return self._lower_text_length_min_value < number

    def _generate_text_length_with_log_normal_distribution(self) -> int:
        mu = np.log(self.mean ** 2 / np.sqrt(self.standard_deviation ** 2 + self.mean ** 2))
        sigma = np.sqrt(np.log(1 + (self.standard_deviation ** 2 / self.mean ** 2)))
        return int(np.random.lognormal(mu, sigma))

    def _generate_bounded_text_length(self) -> int:
        while not self._is_in_bound(text_length := self._generate_text_length_with_log_normal_distribution()):
            pass
        return text_length

    def _generate_upper_text_length(self, text_length: int) -> int:
        return int(text_length + self._min_upper_bound_difference * math.log(text_length, 10))

    def generate_text_length_bounds(self) -> TicketTextLength:
        text_length = self._generate_bounded_text_length()
        return TicketTextLength(lower_bound=text_length, upper_bound=self._generate_upper_text_length(text_length))
