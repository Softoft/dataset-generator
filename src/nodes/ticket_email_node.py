import json
import logging

from ai.chat_assistant import AssistantId, ChatAssistantFactory
from graph.nodes.core.executable_node import ExecutableNode, INode
from graph.nodes.core.inject_storage_objects import inject_storage_objects
from injector import inject
from synthetic_data_generator.ai_graph.data.models import Priority, TicketEmail, TicketExtraInformation, TicketQueue,\
    TicketType
from tenacity import before_sleep_log, retry, retry_if_exception_type, stop_after_attempt

from synthetic_data_generator.ai_graph.key_value_store import KeyValueStore
from synthetic_data_generator.random_generators.number_interval_generator import NumberIntervalGenerator


class TicketEmailNode(ExecutableNode):
    @inject
    def __init__(self, parents: list[INode], text_length_mean: int, text_length_standard_deviation: int):
        self.ticket_email = None
        self.email_generation_assistant = ChatAssistantFactory().create_assistant(AssistantId.EMAIL_GENERATION,
                                                                                  temperature=1.1)
        self.text_length_mean = text_length_mean
        self.text_length_standard_deviation = text_length_standard_deviation
        super().__init__(parents)

    @inject_storage_objects(TicketType, TicketQueue, Priority, TicketExtraInformation)
    async def _execute_node(self, shared_storage: KeyValueStore, ticket_type, ticket_queue, ticket_priority,
                            ticket_extra_information) -> KeyValueStore:
        ticket_email = await self._generate_email(ticket_type, ticket_queue, ticket_priority,
                                                  ticket_extra_information)
        shared_storage.save(ticket_email)
        return shared_storage

    def _generate_email_prompt(self, ticket_type, ticket_queue, priority, ticket_extra_information):
        ticket_body_text_length = NumberIntervalGenerator(self.text_length_mean,
                                                          self.text_length_standard_deviation).generate_bounds()
        ticket_subject_text_length = NumberIntervalGenerator(mean=3, standard_deviation=3,
                                                             lower_number_min_value=-2).generate_bounds()
        is_ticket_subject_empty = ticket_subject_text_length.lower_bound < 0
        subject_text_prompt = f"The subject must have between {ticket_subject_text_length.lower_bound} words" if not is_ticket_subject_empty else "The subject is empty"
        return (
            f"Write an email with a subject and body in JSON Format. To the customer support of a '{ticket_extra_information.business_type}' company."
            f"Write about '{ticket_extra_information.extra_info}', The affected/used product: {ticket_extra_information.product}. "
            f" {ticket_type.get_description()}',"
            f" {ticket_queue.get_description()},"
            f" {priority.get_description()},"
            f"The body must have between '{ticket_body_text_length.lower_bound}' and '{ticket_body_text_length.upper_bound}' words"
            f"{subject_text_prompt}")

    @retry(stop=stop_after_attempt(3), retry=retry_if_exception_type(TypeError),
           before_sleep=before_sleep_log(logging.getLogger(), logging.WARNING))
    async def _generate_email(self, ticket_type: TicketType, ticket_queue: TicketQueue, priority: Priority,
                              ticket_extra_information: TicketExtraInformation):
        prompt = self._generate_email_prompt(ticket_type, ticket_queue, priority,
                                             ticket_extra_information)
        logging.info(f"PROMPT: {prompt}")
        email_json_string = await self.email_generation_assistant.get_response(prompt)
        email_dict = json.loads(email_json_string)
        return TicketEmail(**email_dict)
