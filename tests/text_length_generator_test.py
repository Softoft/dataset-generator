import statistics

import pytest

from graph.data.ticket_text_length import TicketTextLength
from src.text_length_generator import TextLengthGenerator


def get_random_text_length(mean: int, standard_deviation: int, _lower_text_length_min_value: int = 30) -> list[TicketTextLength]:
    text_length_generator = TextLengthGenerator(mean, standard_deviation, _lower_text_length_min_value=_lower_text_length_min_value)
    return [text_length_generator.generate_text_length_bounds() for _ in range(10_000)]


def get_random_numbers(*args, **kwargs) -> list[int]:
    return [text_length.lower_bound for text_length in get_random_text_length(*args, **kwargs)]


@pytest.mark.parametrize("text_length_mean,text_length_standard_deviation", [
    (1_000, 100),
    (100, 100),
    (200, 10),
])
def test_random_text_number_distribution(text_length_mean, text_length_standard_deviation):
    random_numbers = get_random_numbers(text_length_mean, text_length_standard_deviation, _lower_text_length_min_value=0)

    actual_mean = statistics.mean(random_numbers)
    actual_standard_deviation = statistics.stdev(random_numbers)

    assert abs(text_length_mean - actual_mean) < text_length_mean / 2
    assert abs(text_length_standard_deviation - actual_standard_deviation) < text_length_standard_deviation / 2


@pytest.mark.parametrize("_lower_text_length_min_value", [10, 100])
def test_text_random_numbers_are_in_bound(_lower_text_length_min_value):
    mean = 200
    stddev = 1_000
    random_numbers = get_random_numbers(mean, stddev, _lower_text_length_min_value=_lower_text_length_min_value)

    assert min(random_numbers) >= _lower_text_length_min_value


def test_text_length_upper_bound():
    mean = 100
    standard_deviation = 100
    random_text_lengths = get_random_text_length(mean, standard_deviation)
    for random_text_length in random_text_lengths:
        assert random_text_length.upper_bound - random_text_length.lower_bound >= 10
        if random_text_length.lower_bound >= 200:
            assert random_text_length.upper_bound - random_text_length.lower_bound >= 20
            assert random_text_length.upper_bound - random_text_length.lower_bound <= 200
