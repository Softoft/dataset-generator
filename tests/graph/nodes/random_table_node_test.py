import asyncio

import pytest

from conftest import KeyEnum, ValueEnum


def test_execute_random_value(create_random_table_node):
    key_value_weight_dict = {
        KeyEnum.K1: { ValueEnum.V1: 1, ValueEnum.V2: 1, ValueEnum.V3: 1 },
        KeyEnum.K2: { ValueEnum.V1: 1, ValueEnum.V2: 1, ValueEnum.V3: 1 },
    }
    random_table_node = create_random_table_node(KeyEnum.K1, key_value_weight_dict)
    storage = asyncio.run(random_table_node.execute())
    random_value = storage.load(ValueEnum)
    assert random_value in [ValueEnum.V1, ValueEnum.V2, ValueEnum.V3]


def test_execute_random_value_multiple_times(create_random_table_node):
    key_value_weight_dict = {
        KeyEnum.K1: { ValueEnum.V1: 1, ValueEnum.V2: 1, ValueEnum.V3: 1 },
        KeyEnum.K2: { ValueEnum.V1: 1, ValueEnum.V2: 1, ValueEnum.V3: 1 },
    }
    random_table_node = create_random_table_node(KeyEnum.K1, key_value_weight_dict)
    storage = asyncio.run(random_table_node.execute())
    random_value = storage.load(ValueEnum)
    assert random_value in [ValueEnum.V1, ValueEnum.V2, ValueEnum.V3]
    for _ in range(10):
        storage = asyncio.run(random_table_node.execute())
        random_value_2 = storage.load(ValueEnum)
        assert random_value_2 == random_value


@pytest.mark.parametrize("key, weights", [
    (KeyEnum.K1, [1/3, 1/3, 1/3, 1, 1, 1]),
    (KeyEnum.K1, [0.1, 0.8, 0.1, 1, 1, 1]),
    (KeyEnum.K2, [1, 1, 1, 0.4, 0.4, 0.2]),
])
def test_random_node_values_are_random(create_random_table_node, key, weights):
    k1_weights = weights[:3]
    k2_weights = weights[3:]
    key_value_weight_dict = {
        KeyEnum.K1: dict(zip(ValueEnum, k1_weights)),
        KeyEnum.K2: dict(zip(ValueEnum, k2_weights)),
    }
    random_values = [
        asyncio.run(create_random_table_node(key, key_value_weight_dict).execute()).load(ValueEnum)
        for _ in range(1_000)
    ]

    for k, w in zip(ValueEnum, k1_weights if key == KeyEnum.K1 else k2_weights):
        assert abs(random_values.count(k) / len(random_values) - w) < 0.1
