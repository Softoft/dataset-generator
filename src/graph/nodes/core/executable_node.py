import abc
import asyncio
import copy
import logging
from typing import Optional

from util.key_value_storage import KeyValueStorage


class INode(abc.ABC):
    @abc.abstractmethod
    async def execute(self, shared_storage: KeyValueStorage) -> KeyValueStorage:
        pass

    @abc.abstractmethod
    async def _execute_node(self, shared_storage: KeyValueStorage) -> KeyValueStorage:
        pass


class ExecutableNode(INode, abc.ABC):
    def __init__(self, parents: list[INode]):
        self._parents = parents
        self._has_execution_started = False
        self._shared_storage_state: Optional[KeyValueStorage] = None

    async def execute(self, shared_storage: KeyValueStorage = None) -> KeyValueStorage:
        logging.info(f"{self.__class__.__name__} Execute Function called")

        while self._has_execution_started and self._shared_storage_state is None:
            await asyncio.sleep(0.1)
        if self._shared_storage_state is not None:
            logging.info("Already Executed, Returning Changed State")
            return self._shared_storage_state

        logging.info(f"{self.__class__.__name__} Executing")
        self._has_execution_started = True
        shared_storage = shared_storage or KeyValueStorage()
        parent_node_tasks = []
        for parent in self._parents:
            parent_node_tasks.append(parent.execute(copy.deepcopy(shared_storage)))
        parent_storages = list(await asyncio.gather(*parent_node_tasks))
        shared_storage.merge(parent_storages)

        updated_shared_storage = await self._execute_node(shared_storage)
        self._shared_storage_state = copy.deepcopy(updated_shared_storage)
        return updated_shared_storage

    @abc.abstractmethod
    async def _execute_node(self, shared_storage: KeyValueStorage) -> KeyValueStorage:
        pass
