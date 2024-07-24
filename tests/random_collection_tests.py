import enum

from src.ticket_fields.random_collection import RandomCollection, IRandomCollection, RandomCollectionBuilder, \
    RandomTableBuilder


class KeyEnum(enum.Enum):
    K1 = 1
    K2 = 2


class ValueEnum(enum.Enum):
    V1 = 1
    V2 = 2
    V3 = 3


def test_get_random_value():
    VALUES = [ValueEnum.V1, ValueEnum.V2, ValueEnum.V3]
    WEIGHTS = [0.1, 0.3, 0.6]
    random_collection: IRandomCollection = RandomCollection(VALUES, WEIGHTS)

    random_value_list = [random_collection.get_random_value() for _ in range(100_000)]

    for value, weight in zip(VALUES, WEIGHTS):
        assert abs(random_value_list.count(value) / len(random_value_list) - weight) < 0.1


def test_random_enum_collection(random_collection_builder: RandomCollectionBuilder):
    random_enum_collection = random_collection_builder.from_enum(ValueEnum)
    for _ in range(100):
        assert random_enum_collection.get_random_value() in [ValueEnum.V1, ValueEnum.V2, ValueEnum.V3]


def test_random_table(random_table_builder: RandomTableBuilder):
    WEIGHTS_K1 = [0.1, 0.3, 0.6]
    WEIGHTS_K2 = [0.4, 0.4, 0.2]
    random_table_builder.add_value_weight_2d(KeyEnum, ValueEnum, [WEIGHTS_K1, WEIGHTS_K2])
    random_table = random_table_builder.build()

    values_from_key1 = [random_table.get_random_value(KeyEnum.K1) for _ in range(10_000)]
    values_from_key2 = [random_table.get_random_value(KeyEnum.K2) for _ in range(10_000)]

    for weight, value in zip(WEIGHTS_K1, ValueEnum):
        assert abs(values_from_key1.count(value) / len(values_from_key1) - weight) < 0.1

    for weight, value in zip(WEIGHTS_K2, ValueEnum):
        assert abs(values_from_key2.count(value) / len(values_from_key2) - weight) < 0.1



