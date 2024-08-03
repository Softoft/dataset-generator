import asyncio
import statistics

import pytest

from graph.data.models import NumberInterval
from util.number_interval_generator import NumberIntervalGenerator


def test_equal_method():
    number_interval_1 = NumberInterval(10, 20)
    number_interval_2 = NumberInterval(10, 20)
    assert number_interval_1 == number_interval_2

    number_interval_3 = NumberInterval(10, 20)
    number_interval_4 = NumberInterval(10, 21)
    assert number_interval_3 != number_interval_4


def test_intervals_are_random(create_text_length_node):
    random_s = []
    mean = 400
    standard_deviation = 200
    for _ in range(200):
        text_length_node = create_text_length_node(mean, standard_deviation)
        shared_storage = asyncio.run(text_length_node.execute())
        random_s.append(shared_storage.get(NumberInterval))

    lower_bounds = [text_length.lower_bound for text_length in random_s]
    upper_bounds = [text_length.upper_bound for text_length in random_s]

    upper_lower_difference = [upper_bound - lower_bound for upper_bound, lower_bound in zip(upper_bounds, lower_bounds)]
    assert min(upper_lower_difference) >= 10
    assert max(upper_lower_difference) >= 20
    assert min(upper_lower_difference) + 10 < max(upper_lower_difference)

    assert abs(statistics.mean(lower_bounds) - mean) < mean / 2
    assert abs(statistics.stdev(lower_bounds) - standard_deviation) < standard_deviation / 2


def get_random_interval(mean: int, standard_deviation: int, _lower_number_min_value: int = 0) -> list[NumberInterval]:
    number_interval_generator = NumberIntervalGenerator(mean, standard_deviation,
                                                        lower_number_min_value=_lower_number_min_value)
    return [number_interval_generator.generate_bounds() for _ in range(10_000)]


def get_random_numbers(*args, **kwargs) -> list[int]:
    return [text_length.lower_bound for text_length in get_random_interval(*args, **kwargs)]


@pytest.mark.parametrize("text_length_mean,text_length_standard_deviation", [
    (1_000, 100),
    (100, 100),
    (200, 10),
])
def test_random_interval_distribution(text_length_mean, text_length_standard_deviation):
    random_numbers = get_random_numbers(text_length_mean, text_length_standard_deviation,
                                        _lower_text_length_min_value=0)

    actual_mean = statistics.mean(random_numbers)
    actual_standard_deviation = statistics.stdev(random_numbers)

    assert abs(text_length_mean - actual_mean) < text_length_mean / 2
    assert abs(text_length_standard_deviation - actual_standard_deviation) < text_length_standard_deviation / 2


@pytest.mark.parametrize("_lower_number_min_value", [10, 100])
def test_random_numbers_intervals_are_in_bound(_lower_number_min_value):
    mean = 200
    stddev = 1_000
    random_numbers = get_random_numbers(mean, stddev, _lower_text_length_min_value=_lower_number_min_value)

    assert min(random_numbers) >= _lower_number_min_value


def test_text_length_upper_bound():
    mean = 100
    standard_deviation = 100
    random_text_lengths = get_random_interval(mean, standard_deviation)
    for random_text_length in random_text_lengths:
        assert random_text_length.upper_bound - random_text_length.lower_bound >= 10
        if random_text_length.lower_bound >= 200:
            assert random_text_length.upper_bound - random_text_length.lower_bound >= 20
            assert random_text_length.upper_bound - random_text_length.lower_bound <= 200
