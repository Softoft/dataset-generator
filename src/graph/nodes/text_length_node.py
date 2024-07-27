from typing import Optional

from graph.data.ticket_text_length import TicketTextLength
from graph.nodes.executable_node import ExecutableNode
from graph.nodes.state_full_node import save_execute_state
from storage.key_value_storage import KeyValueStorage
from text_length_generator import TextLengthGenerator


class TextLengthNode(ExecutableNode):
    def __init__(self, text_length_generator: TextLengthGenerator):
        self.text_length_generator = text_length_generator
        self.text_length: Optional[TicketTextLength] = None
        super().__init__([])

    @save_execute_state(lambda self: self.text_length)
    def execute(self, shared_storage: KeyValueStorage = None) -> KeyValueStorage:
        return super().execute(shared_storage)

    def _execute_node(self, shared_storage: KeyValueStorage) -> KeyValueStorage:
        self.text_length: TicketTextLength = self.text_length_generator.generate_text_length_bounds()
        shared_storage.save(self.text_length)
        return shared_storage


