import pytest

from src.text_length_generator import TextLengthGenerator
from src.ticket_fields.random_collection import RandomCollectionBuilder, RandomTableBuilder


@pytest.fixture
def text_length_generator():
    return TextLengthGenerator(1000, 100)


@pytest.fixture
def random_collection_builder():
    return RandomCollectionBuilder()


@pytest.fixture
def random_table_builder():
    return RandomTableBuilder()
