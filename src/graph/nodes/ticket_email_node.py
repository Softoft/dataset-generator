from graph.data.priority import Priority
from graph.data.ticket_queue import TicketQueue
from graph.data.ticket_text_length import TicketTextLength
from graph.data.ticket_type import TicketType
from graph.nodes.executable_node import ExecutableNode, INode
from graph.nodes.state_full_node import save_state
from prompt_generation.prompt_generator import PromptGenerator
from storage.key_value_storage import KeyValueStorage


class TicketEmailNode(ExecutableNode):
    def __init__(self, parents: list[INode]):
        self.ticket_email = None
        self.prompt_generator = PromptGenerator()
        super().__init__(parents)

    @save_state(lambda self: self.ticket_email)
    def execute(self, shared_storage: KeyValueStorage = None) -> KeyValueStorage:
        return super().execute(shared_storage)

    def _execute_node(self, shared_storage: KeyValueStorage) -> KeyValueStorage:
        ticket_type = shared_storage.load(TicketType)
        ticket_queue = shared_storage.load(TicketQueue)
        ticket_priority = shared_storage.load(Priority)
        ticket_text_length = shared_storage.load(TicketTextLength)
        prompt = self.prompt_generator.create_prompt(ticket_type, ticket_queue, ticket_priority, ticket_text_length)

        return shared_storage
