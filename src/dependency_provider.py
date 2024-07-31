from typing import Callable

from injector import Module, provider, singleton

from config import Config
from graph.graph_ticket_generator import GraphTicketGenerator
from graph.nodes.ticket_rewriting_translating_node import TextSimilarityThreshold, TextSimilarityThresholds
from ticket_generator.ticket_generator import TicketGenerator


class TicketGenerationModule(Module):
    @singleton
    @provider
    def provide_ticket_generation_config(self) -> Config:
        return Config(
            number_of_tickets=1000,
            output_file="../data/training/dataset-v3_26_0-big.json",
            number_translation_nodes=4,
            batch_size=10,
            text_length_mean=40,
            text_length_standard_deviation=20,
            text_similarity_thresholds=TextSimilarityThresholds([
                TextSimilarityThreshold(100, 0.9),
                TextSimilarityThreshold(30, 0.95),
                TextSimilarityThreshold(0, 1),
            ]))

    @singleton
    @provider
    def provide_graph_ticket_generator_factory(self, ticket_generation_config: Config) -> Callable[
        [], GraphTicketGenerator]:
        return lambda: GraphTicketGenerator(ticket_generation_config)

    @singleton
    @provider
    def provide_ticket_generator(self, ticket_generation_config: Config,
                                 graph_ticket_generator_factory: Callable[[], GraphTicketGenerator]) -> TicketGenerator:
        return TicketGenerator(ticket_generation_config, graph_ticket_generator_factory)
