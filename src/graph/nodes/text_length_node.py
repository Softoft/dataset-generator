import dataclasses
import math

import numpy as np

from graph.data.models import TicketTextLength
from graph.key_value_storage import KeyValueStorage
from graph.nodes.core.executable_node import ExecutableNode


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
        text_length = self._generate_text_length_with_log_normal_distribution()
        while not self._is_in_bound(text_length):
            text_length = self._generate_text_length_with_log_normal_distribution()
        return text_length

    def _generate_upper_text_length(self, text_length: int) -> int:
        return int(text_length + self._min_upper_bound_difference * math.log(text_length, 10))

    def generate_text_length_bounds(self) -> TicketTextLength:
        text_length = self._generate_bounded_text_length()
        return TicketTextLength(lower_bound=text_length, upper_bound=self._generate_upper_text_length(text_length))


class TextLengthNode(ExecutableNode):
    def __init__(self, text_length_generator: TextLengthGenerator):
        self.text_length_generator = text_length_generator
        super().__init__([])

    async def _execute_node(self, shared_storage: KeyValueStorage) -> KeyValueStorage:
        shared_storage.save(self.text_length_generator.generate_text_length_bounds())
        return shared_storage
