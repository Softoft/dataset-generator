from graph.nodes.text_length_node import TextLengthNode
from text_length_generator import TextLengthGenerator


def create_text_length_node(mean: int, standard_deviation: int) -> TextLengthNode:
    text_length_generator = TextLengthGenerator(mean=mean, standard_deviation=standard_deviation)
    return TextLengthNode(text_length_generator)