from src.graph.executable_node import ExecutableNode


class RandomNode(ExecutableNode):
    def __init__(self, parents):
        super().__init__(parents)

    async def _execute_node(self):
        pass