import abc
import asyncio

from src.graph.storage import KeyValueStorage


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
        self._was_executed = False

    @abc.abstractmethod
    async def _execute_node(self, shared_storage: KeyValueStorage) -> KeyValueStorage:
        pass

    async def execute(self, shared_storage: KeyValueStorage = None) -> KeyValueStorage:
        if shared_storage is None:
            shared_storage = KeyValueStorage()
        if self._was_executed:
            return shared_storage

        parent_execution_tasks = [parent.execute(shared_storage.deepcopy()) for parent in self._parents]
        parent_storages = list(await asyncio.gather(*parent_execution_tasks))
        merged_storage = KeyValueStorage()
        merged_storage.merge([shared_storage] + parent_storages)

        updated_shared_storage = await self._execute_node(merged_storage)
        self._was_executed = True
        return updated_shared_storage
