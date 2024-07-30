from dataclasses import dataclass

from graph.nodes.ticket_rewriting_translating_node import TextSimilarityThresholds


@dataclass
class TicketGenerationConfig:
    number_of_tickets: int
    output_file: str
    number_translation_nodes: int
    text_length_mean: int
    text_length_standard_deviation: int
    batch_size: int
    text_similarity_thresholds: TextSimilarityThresholds


class SemanticVersion:
    def __init__(self, major=0, minor=0, patch=0):
        self.major = major
        self.minor = minor
        self.patch = patch

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"

    def increase_major(self):
        self.major += 1
        self.minor = 0
        self.patch = 0

    def increase_minor(self):
        self.minor += 1
        self.patch = 0

    def increase_patch(self):
        self.patch += 1
