import abc
import logging
from typing import Optional

from graph.key_value_storage import KeyValueStorage


class INode(abc.ABC):
    @abc.abstractmethod
    def execute(self, shared_storage: KeyValueStorage) -> KeyValueStorage:
        pass

    @abc.abstractmethod
    def _execute_node(self, shared_storage: KeyValueStorage) -> KeyValueStorage:
        pass


class ExecutableNode(INode, abc.ABC):
    def __init__(self, parents: list[INode]):
        self.__parents = parents
        self.__shared_storage_state: Optional[KeyValueStorage] = None

    def execute(self, shared_storage: KeyValueStorage = None) -> KeyValueStorage:
        logging.info("Executing")
        shared_storage = shared_storage or KeyValueStorage()
        if self.__shared_storage_state:
            logging.info("Already Executed, Returning Changed State")
            return self.__shared_storage_state

        parent_storages = [parent.execute(shared_storage.deepcopy()) for parent in self.__parents]
        shared_storage.merge(parent_storages)

        updated_shared_storage = self._execute_node(shared_storage)
        self.__shared_storage_state = updated_shared_storage.deepcopy()
        return updated_shared_storage

    @abc.abstractmethod
    def _execute_node(self, shared_storage: KeyValueStorage) -> KeyValueStorage:
        pass
