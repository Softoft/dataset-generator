import statistics

from graph.data.ticket_text_length import TicketTextLength


def test_text_length_node(create_text_length_node):
    text_length_node = create_text_length_node(400, 400)
    shared_storage = text_length_node.execute()
    assert shared_storage.load(TicketTextLength) is not None


def test_ticket_text_length_equal_method():
    ticket_text_length_1 = TicketTextLength(10, 20)
    ticket_text_length_2 = TicketTextLength(10, 20)
    assert ticket_text_length_1 == ticket_text_length_2

    ticket_text_length_3 = TicketTextLength(10, 20)
    ticket_text_length_4 = TicketTextLength(10, 21)
    assert ticket_text_length_3 != ticket_text_length_4


def test_text_length_node_results_are_saved(create_text_length_node):
    text_length_node = create_text_length_node(400, 400)
    shared_storage = text_length_node.execute()
    text_length_1 = shared_storage.load(TicketTextLength)
    assert text_length_1 is not None
    shared_storage = text_length_node.execute()
    text_length_2 = shared_storage.load(TicketTextLength)
    assert text_length_2 is not None
    assert text_length_1 == text_length_2


def test_ticket_text_lengths_are_random(create_text_length_node):
    random_ticket_text_lengths = []
    mean = 400
    standard_deviation = 200
    for _ in range(1_000):
        text_length_node = create_text_length_node(mean, standard_deviation)
        shared_storage = text_length_node.execute()
        random_ticket_text_lengths.append(shared_storage.load(TicketTextLength))

    lower_bounds = [text_length.lower_bound for text_length in random_ticket_text_lengths]
    upper_bounds = [text_length.upper_bound for text_length in random_ticket_text_lengths]

    upper_lower_difference = [upper_bound - lower_bound for upper_bound, lower_bound in zip(upper_bounds, lower_bounds)]
    assert min(upper_lower_difference) >= 10
    assert max(upper_lower_difference) >= 20
    assert min(upper_lower_difference) + 10 < max(upper_lower_difference)

    assert abs(statistics.mean(lower_bounds) - mean) < mean / 2
    assert abs(statistics.stdev(lower_bounds) - standard_deviation) < standard_deviation / 2
