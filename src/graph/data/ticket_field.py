import abc
from enum import Enum


class ComparableEnum(Enum):
    def __eq__(self, other):
        try:
            return self.value == other.value
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.value)


class InputTicketField:
    @abc.abstractmethod
    def get_description(self):
        pass


class CategoricalTicketField(InputTicketField, ComparableEnum):
    def __new__(cls, value, description):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.description = description
        return obj

    def get_description(self):
        return self.description
