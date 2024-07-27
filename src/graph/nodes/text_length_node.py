from graph.nodes.core.executable_node import ExecutableNode
from graph.key_value_storage import KeyValueStorage
from text_length_generator import TextLengthGenerator


class TextLengthNode(ExecutableNode):
    def __init__(self, text_length_generator: TextLengthGenerator):
        self.text_length_generator = text_length_generator
        super().__init__([])

    async def _execute_node(self, shared_storage: KeyValueStorage) -> KeyValueStorage:
        shared_storage.save(self.text_length_generator.generate_text_length_bounds())
        return shared_storage
