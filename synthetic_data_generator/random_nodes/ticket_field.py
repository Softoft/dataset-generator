import abc
from dataclasses import dataclass, fields
from enum import Enum
from typing import get_type_hints

from synthetic_data_generator.random_generators.random_collection import RandomCollectionFactory


class ComparableEnum(Enum):
    def __eq__(self, other):
        try:
            return self.value == other.value
        except AttributeError:
            return False

    def __hash__(self):
        return hash(self.value)


class InputModel:
    @abc.abstractmethod
    def get_description(self):
        pass


class RandomDescriptionModel(InputModel, ComparableEnum):
    def __init__(self, value, descriptions):
        self._value_ = value
        self.descriptions = descriptions
        super().__init__(value)

    def get_description(self):
        RandomCollectionFactory().build_from_list_of_values(self.descriptions).get_random_value()


@dataclass
class OutputDataclassModel:
    @classmethod
    def list_attributes_and_types(cls):
        type_hints = get_type_hints(cls)
        attributes = fields(cls)
        return ", ".join(f"{attr.name}: {type_hints[attr.name].__name__}" for attr in attributes)


class CategoricalModel(InputModel, ComparableEnum):
    def __new__(cls, value, description):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.description = description
        return obj

    def get_description(self):
        return self.description
