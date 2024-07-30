from typing import Callable

from injector import Module, provider, singleton

from config import TicketGenerationConfig
from graph.graph_ticket_generator import GraphTicketGenerator
from graph.nodes.ticket_rewriting_and_translating_node import TextSimilarityThreshold, TextSimilarityThresholds
from ticket_generator.ticket_generator import TicketGenerator


class TicketGenerationModule(Module):
    @singleton
    @provider
    def provide_ticket_generation_config(self) -> TicketGenerationConfig:
        return TicketGenerationConfig(
            number_of_tickets=10,
            output_file="../data/training/dataset-v3_14_0-test.json",
            number_translation_nodes=10,
            batch_size=1,
            text_length_mean=30,
            text_length_standard_deviation=10,
            text_similarity_thresholds=TextSimilarityThresholds([
                TextSimilarityThreshold(100, 0.7),
                TextSimilarityThreshold(30, 0.8),
                TextSimilarityThreshold(0, 1),
            ]))

    @singleton
    @provider
    def provide_graph_ticket_generator_factory(self, ticket_generation_config: TicketGenerationConfig) -> Callable[
        [], GraphTicketGenerator]:
        return lambda: GraphTicketGenerator(ticket_generation_config)

    @singleton
    @provider
    def provide_ticket_generator(self, ticket_generation_config: TicketGenerationConfig,
                                 graph_ticket_generator_factory: Callable[[], GraphTicketGenerator]) -> TicketGenerator:
        return TicketGenerator(ticket_generation_config, graph_ticket_generator_factory)
