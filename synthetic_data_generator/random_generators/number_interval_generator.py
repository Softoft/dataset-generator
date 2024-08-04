import logging
import math
from dataclasses import dataclass

import numpy as np
from pydantic import BaseModel, Field


@dataclass
class NumberInterval:
    lower_bound: float
    upper_bound: float

    def __contains__(self, item: float | int):
        return self.lower_bound <= item <= self.upper_bound

    def __eq__(self, other):
        return self.lower_bound == other.lower_bound and self.upper_bound == other.upper_bound

    def __hash__(self):
        return hash((self.lower_bound, self.upper_bound))


class NormalizedNumberGenerator(BaseModel):
    """
    Generates a random normal distributed number.
    Args:
        mean (float):
        number_bounds (NumberInterval):
        standard_deviation (float):
    """
    mean: float
    number_bounds: NumberInterval = Field(default=NumberInterval(-10 ** 40, 10 ** 40))
    standard_deviation: float = Field(gt=0)

    def _generate_random_normal_distribution_number(self) -> int:
        return round(np.random.normal(self.mean, self.standard_deviation))

    def generate_bounded_number(self) -> int:
        number = self._generate_random_normal_distribution_number()
        while number not in self.number_bounds:
            number = self._generate_random_normal_distribution_number()
        return number


class NumberIntervalGenerator(BaseModel):
    """
    Generates a random number interval based on a normal distribution.
    Attributes:
        mean (float): The mean of the normal distribution.
        standard_deviation (float): The standard deviation of the normal distribution.
        min_upper_bound_difference (float): The minimum difference between the lower and upper bounds.
        lower_number_bounds (NumberInterval): The bounds for the lower number.
        lower_number_generator (NormalizedNumberGenerator): Optional. The generator for the lower number.
    """
    mean: float
    standard_deviation: float = Field(gt=0)
    min_upper_bound_difference: float = Field(ge=0)
    lower_number_bounds: NumberInterval = Field(default=NumberInterval(0, 10 ** 12))
    lower_number_generator: NormalizedNumberGenerator = None

    def model_post_init(self, __context: any) -> None:
        if self.lower_number_generator is None:
            self.lower_number_generator: NormalizedNumberGenerator = NormalizedNumberGenerator(
                number_bounds=self.lower_number_bounds,
                mean=self.mean,
                standard_deviation=self.standard_deviation
            )

    def _generate_upper_bound(self, lower_bound: int) -> int:
        upper_bound_factor = math.log2(max(2, abs(lower_bound)))
        return round(lower_bound + self.min_upper_bound_difference * upper_bound_factor)

    def generate_bounds(self) -> NumberInterval:
        lower_bound = self.lower_number_generator.generate_bounded_number()
        upper_bound = self._generate_upper_bound(lower_bound)
        logging.info(f"Generated number interval: {lower_bound}, {upper_bound}")
        return NumberInterval(lower_bound=lower_bound, upper_bound=upper_bound)
