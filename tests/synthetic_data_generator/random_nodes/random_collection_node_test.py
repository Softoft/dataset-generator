import asyncio

from conftest import ValueEnum


def test_random_collection_node(create_random_collection_node):
    random_collection_node = create_random_collection_node({ValueEnum.V1: 1, ValueEnum.V2: 2, ValueEnum.V3: 3})
    assert random_collection_node.random_generator.get_random_value() in [ValueEnum.V1, ValueEnum.V2, ValueEnum.V3]


def test_random_collection_node_multiple_times(create_random_collection_node):
    random_collection_node = create_random_collection_node({ValueEnum.V1: 1, ValueEnum.V2: 2, ValueEnum.V3: 3})
    random_value = asyncio.run(random_collection_node.execute()).get(ValueEnum)
    for _ in range(10):
        assert asyncio.run(random_collection_node.execute()).get(ValueEnum) == random_value

