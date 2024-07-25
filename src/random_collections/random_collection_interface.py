import abc
from enum import Enum


class IRandom[V: Enum](abc.ABC):
    def get_random_value(self, *args, **kwargs) -> V:
        pass
