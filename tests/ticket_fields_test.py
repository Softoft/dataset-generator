from graph.data.ticket_field import CategoricalTicketField

from synthetic_data_generator.random_generators.random_collection import RandomCollectionFactory


class MyTicketField(CategoricalTicketField):
    LOW = 1, "description low"
    MEDIUM = 2, "description medium"
    HIGH = 3, "description high"


def test_categorical_field():
    high_value = MyTicketField.HIGH
    print(high_value)
    assert high_value.description == "description high"


def test_categorical_field_random_collection():
    random_collection = RandomCollectionFactory.build_from_value_weight_dict(
        { MyTicketField.LOW: 1, MyTicketField.MEDIUM: 1, MyTicketField.HIGH: 2 }
    )
    for _ in range(1_000):
        random_value = random_collection.get_random_value()
        assert random_value in [MyTicketField.LOW, MyTicketField.MEDIUM, MyTicketField.HIGH]
        assert random_value.description is not None
