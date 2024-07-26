from graph.core.executable_node import ExecutableNode
from graph.core.state_full_node import save_state
from storage.key_value_storage import KeyValueStorage
from text_length_generator import TextLengthGenerator


class TextLengthNode(ExecutableNode):
    def __init__(self, text_length_generator: TextLengthGenerator):
        self.text_length_generator = text_length_generator
        self.text_length = None
        super().__init__([])

    @save_state(lambda self: self.text_length)
    def execute(self, shared_storage: KeyValueStorage = None) -> KeyValueStorage:
        return super().execute(shared_storage)

    def _execute_node(self, shared_storage: KeyValueStorage) -> KeyValueStorage:
        pass


