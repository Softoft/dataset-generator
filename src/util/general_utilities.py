from functools import reduce


def union_dicts(*dicts):
    return reduce(lambda a, b: { **a, **b }, dicts)
