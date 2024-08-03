import json
from typing import Callable

from injector import Module, provider, singleton

from config import Config
from graph.graph_ticket_generator import GraphTicketGenerator
from graph.nodes.ticket_rewriting_translating_node import TextSimilarityThreshold, TextSimilarityThresholds
from ticket_generator.ticket_generator import TicketGenerator
from util.text_similarity_calculator import SimilarityCalculator


class TicketGenerationModule(Module):
    @singleton
    @provider
    def provide_ticket_generation_config(self) -> Config:
        config_object = json.load(open("config.json", "w"))
        text_similarity_thresholds = TextSimilarityThresholds([
            TextSimilarityThreshold(
                threshold["length"],
                threshold["similarity"]
            ) for threshold in config_object["text_similarity_thresholds"]
        ])

        return Config(
            number_of_tickets=1_000,
            output_file="../data/training/dataset-v3_27_3-big-release.json",
            number_translation_nodes=5,
            batch_size=50,
            text_length_mean=50,
            text_length_standard_deviation=30,
            max_text_similarity=0.9,
            min_content_similarity=0.3,
        )

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
