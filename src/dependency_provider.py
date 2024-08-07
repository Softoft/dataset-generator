from typing import Callable

from injector import Module, provider, singleton
from openai import AsyncOpenAI

from config import Config
from graph_ticket_generator import GraphTicketGenerator
from synthetic_data_generator.ai_graph.ai.chat_assistant import ChatAssistant
from synthetic_data_generator.ai_graph.ai.chat_assistant_config import AssistantModel
from synthetic_data_generator.random_generators.number_interval_generator import NumberInterval
from text_similarity_calculator import SimilarityCalculator, TicketParaphraseValidator
from ticket_generator.ticket_generator import TicketGenerator


class TicketGenerationModule(Module):
    @singleton
    @provider
    def provide_graph_ticket_generator_factory(self, config: Config) -> Callable[[], GraphTicketGenerator]:
        return lambda: GraphTicketGenerator(config)

    @singleton
    @provider
    def provide_ticket_generator(self, ticket_generation_config: Config,
                                 graph_ticket_generator_factory: Callable[[], GraphTicketGenerator]) -> TicketGenerator:
        return TicketGenerator(ticket_generation_config, graph_ticket_generator_factory)

    @singleton
    @provider
    def provide_similarity_calculator(self) -> SimilarityCalculator:
        return SimilarityCalculator()

    @singleton
    @provider
    def provide_async_openai(self) -> AsyncOpenAI:
        return AsyncOpenAI()

    @singleton
    @provider
    def provide_create_assistant(self, async_openai: AsyncOpenAI) -> Callable[
        [str, str, AssistantModel, float], ChatAssistant]:
        def assistant_factory(name: str, _id: str, model: AssistantModel, temperature: float):
            return ChatAssistant(assistant_name=name, assistant_id=_id, model=model, temperature=temperature,
                                 client=async_openai)

        return assistant_factory

    @singleton
    @provider
    def provide_similarity_calculator(self) -> SimilarityCalculator:
        return SimilarityCalculator()

    @singleton
    @provider
    def provide_ticket_paraphrase_validator_factory(self, similarity_calculator: SimilarityCalculator) -> (Callable[
        [NumberInterval, NumberInterval], TicketParaphraseValidator]):
        def factory(text_similarity_bounds: NumberInterval, content_similarity_bounds: NumberInterval):
            return TicketParaphraseValidator(text_similarity_bounds, content_similarity_bounds, similarity_calculator)

        return factory
