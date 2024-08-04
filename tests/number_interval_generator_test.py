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


def test_contains_method():
    number_interval = NumberInterval(10, 20)
    assert 10 in number_interval
    assert 20 in number_interval
    assert 15 in number_interval
    assert 9 not in number_interval
    assert 21 not in number_interval

    number_interval_negative = NumberInterval(-20.1, 10.1)
    assert -20.1 in number_interval_negative
    assert 0.1 in number_interval_negative


@pytest.mark.parametrize("mean,standard_deviation", [
    (1_000, 100),
    (100, 100),
    (200, 10),
])
def test_random_interval_distribution(mean, standard_deviation, get_random_numbers):
    random_numbers = get_random_numbers(mean, standard_deviation, NumberInterval(-10 ** 40, 10 ** 40), amount=100_000)

    actual_mean = statistics.mean(random_numbers)
    actual_standard_deviation = statistics.stdev(random_numbers)

    assert abs(mean - actual_mean) < mean / 100
    assert abs(standard_deviation - actual_standard_deviation) < standard_deviation / 100


@pytest.mark.parametrize("number_bound_lower,number_bound_upper,mean,standard_deviation",
                         [
                             (-20, 100, 50, 100),
                             (0, 200, 100, 200),
                             (-10_000.1, -1000.23, -5000, 10_000),
                             (-10, 1, 0.999, 0.001),
                             (-1, 10, -0.999, 0.001),
                         ])
def test_random_numbers_are_in_bound(number_bound_lower, number_bound_upper, mean, standard_deviation,
                                     get_random_numbers):
    number_bound = NumberInterval(number_bound_lower, number_bound_upper)
    random_numbers = get_random_numbers(mean, standard_deviation, number_bound)
    assert all([number in number_bound for number in random_numbers])


@pytest.mark.parametrize("lower_value1,lower_value2,min_upper_bound_difference", [
    (10, 100, 10),
    (2, 100, 1),
    (1, 50, 1),
    (0, 50, 1),
    (-1, 50, 1),
    (3, 100, 2),
    (30, 40, 3),
])
def test_random_number_interval_generator(lower_value1, lower_value2, min_upper_bound_difference,
                                          get_mocked_random_interval):
    number_interval_generator: NumberIntervalGenerator = get_mocked_random_interval(lower_value1,
                                                                                    min_upper_bound_difference)
    number_interval = number_interval_generator.generate_bounds()
    assert number_interval.lower_bound == lower_value1
    low_num_diff = number_interval.upper_bound - number_interval.lower_bound
    assert low_num_diff >= min_upper_bound_difference

    number_interval_generator: NumberIntervalGenerator = get_mocked_random_interval(lower_value2,
                                                                                    min_upper_bound_difference)
    number_interval = number_interval_generator.generate_bounds()
    assert number_interval.lower_bound == lower_value2
    high_num_diff = number_interval.upper_bound - number_interval.lower_bound
    assert high_num_diff >= min_upper_bound_difference
    assert high_num_diff > low_num_diff
