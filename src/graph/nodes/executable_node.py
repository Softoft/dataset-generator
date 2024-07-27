import abc
import asyncio
import logging

from storage.key_value_storage import KeyValueStorage


class INode(abc.ABC):
    @abc.abstractmethod
    def execute(self, shared_storage: KeyValueStorage) -> KeyValueStorage:
        pass

    @abc.abstractmethod
    def _execute_node(self, shared_storage: KeyValueStorage) -> KeyValueStorage:
        pass


class ExecutableNode(INode, abc.ABC):
    def __init__(self, parents: list[INode]):
        self._parents = parents
        self.permanently_saved = None
        self._was_executed = False

    def execute(self, shared_storage: KeyValueStorage = None) -> KeyValueStorage:
        logging.info("Executing")
        shared_storage = shared_storage or KeyValueStorage()
        if self._was_executed:
            logging.info("Already executed")
            return shared_storage

        parent_storages = [parent.execute(shared_storage.deepcopy()) for parent in self._parents]
        shared_storage.merge(parent_storages)

        updated_shared_storage = self._execute_node(shared_storage)
        self._was_executed = True
        return updated_shared_storage

    @abc.abstractmethod
    def _execute_node(self, shared_storage: KeyValueStorage) -> KeyValueStorage:
        pass
