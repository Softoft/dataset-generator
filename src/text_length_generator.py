import dataclasses
import math

import numpy as np

rng = np.random.default_rng(seed=42)


@dataclasses.dataclass
class TextLengthGenerator:
    mean: int
    std_dev: int
    lower_bound: int = 30
    upper_bound: int = 10 ** 5
    min_text_length_diff: int = 15

    def __post_init__(self):
        assert self._is_in_bound(self.mean), "Mean is out of bounds"
        assert self.lower_bound >= 0, "Lower bound is negative"

    def _is_in_bound(self, number: float | int):
        return self.lower_bound < number < self.upper_bound

    def _generate_text_length(self):
        mu = np.log(self.mean ** 2 / np.sqrt(self.std_dev ** 2 + self.mean ** 2))
        sigma = np.sqrt(np.log(1 + (self.std_dev ** 2 / self.mean ** 2)))
        return int(np.random.lognormal(mu, sigma))

    def generate_bounded_text_length(self):
        text_length = self._generate_text_length()
        while not self._is_in_bound(text_length):
            text_length = self._generate_text_length()
        return text_length

    def _generate_upper_text_length(self, text_length: int):
        return text_length + math.log(text_length) * self.min_text_length_diff

    def generate_text_length_bounds(self):
        text_length = self.generate_bounded_text_length()

        return text_length, self._generate_upper_text_length(text_length)
