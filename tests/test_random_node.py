import asyncio

from conftest import ValueEnum
from graph.random_node import RandomTableNode


def test_execute_random_value(random_table_node: RandomTableNode):
	storage = asyncio.run(random_table_node.execute())
	random_value = storage.load(ValueEnum)
	assert random_value in [ValueEnum.V1, ValueEnum.V2]

