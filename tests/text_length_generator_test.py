import statistics

import pytest

from src.text_length_generator import TextLengthGenerator


def get_random_numbers_from_text_length_generator(*args, **kwargs):
    text_length_generator = TextLengthGenerator(*args, **kwargs)
    return [text_length_generator.generate_bounded_text_length() for _ in range(10_000)]


@pytest.mark.parametrize("text_length_mean,text_length_std_dev", [
    (1_000, 100),
    (100, 100),
    (200, 10),
])
def test_random_text_number_distribution(text_length_mean, text_length_std_dev):
    random_numbers = get_random_numbers_from_text_length_generator(text_length_mean, text_length_std_dev, lower_bound=0)

    actual_mean = statistics.mean(random_numbers)
    actual_std_dev = statistics.stdev(random_numbers)

    assert abs(text_length_mean - actual_mean) < text_length_mean / 2
    assert abs(text_length_std_dev - actual_std_dev) < text_length_std_dev / 2


@pytest.mark.parametrize("lower_bound,upper_bound", [
    (10, 300),
    (100, 1_000),
])
def test_text_random_numbers_are_in_bound(lower_bound, upper_bound):
    mean = 200
    stddev = 1_000
    random_numbers = get_random_numbers_from_text_length_generator(mean, stddev, lower_bound=lower_bound,
                                                                   upper_bound=upper_bound)

    assert min(random_numbers) >= lower_bound
    assert max(random_numbers) <= upper_bound
