import logging
from unittest.mock import Mock

import pytest

from config import Config
from text_similarity_calculator import SimilarityCalculator,\
    TicketParaphraseValidator


def log_similarity(text1, text2):
    similarity = SimilarityCalculator().get_text_similarity(text1, text2)
    logging.info(f"'{text1}' and '{text2}': word frequency {round(similarity, 4)}")
    return similarity


def test_returns_correct_similarity_for_identical_texts():
    result = log_similarity("same text", "same text")
    assert pytest.approx(result) == 1.0


@pytest.mark.parametrize("text1,text2,expected", [
    ("This is a house", "This is a boat", 0.8),
    ("Where is my car?", "Here is my car", 0.8),
    ("This text only has one difference", "This text only one has difference", 0.8),
    ("My car is red", "My car is blue", 0.8),
    ("I hate this car!", "I love this car!", 0.8),
    ("I hate this car!", "I hate this car, because its red", 0.8),
    (
            "This test checks how the text similarity function is working! I do not really understand how these values are calculated",
            "This test checks how the text similarity function is working! I do not really understand how this value is calculated",
            0.6),
    ("My man is driving me crazy", "My man is driving a car", 0.6),
    ("These two texts almost have nothing in common", "Because only one word is the same: texts", 0.1),
    ("These two texts have nothing in common", "Because no words are same", 0),
])
def test_returns_correct_similarity_for_texts(text1, text2, expected):
    result = log_similarity(text1, text2)
    assert abs(result - expected) < 0.1


@pytest.mark.parametrize(
    "similar_text_pair,less_similar_text_pair",
    [
        (("I like to go to school", "I like going to my school"),
         ("My favorite color is blue", "I like to go to school")),
        (("The quick brown fox jumps over the lazy dog", "A quick brown fox jumps over a lazy dog"),
         ("The sun is shining brightly", "I love rainy days")),
        (("She sells seashells by the seashore", "She sells seashells on the seashore"),
         ("He loves to play football", "She enjoys reading books"))
    ])
def test_similarity_scores_of_texts(similar_text_pair, less_similar_text_pair):
    similar_text_pair_score = SimilarityCalculator().get_content_similarity(similar_text_pair[0], similar_text_pair[1])

    less_similar_text_pair_score = SimilarityCalculator().get_content_similarity(less_similar_text_pair[0],
                                                                                 less_similar_text_pair[1])
    logging.info(f"{similar_text_pair[0]}; {similar_text_pair[1]} => {similar_text_pair_score}")
    logging.info(f"Similarity score of less similar text pair: {less_similar_text_pair_score}")
    assert similar_text_pair_score > less_similar_text_pair_score


@pytest.mark.parametrize("text1,text2", [
    ("This is a good paraphrasing", "This is a valid paraphrasing"),
    ("I like my car, its my favorite color", "I love my car, it has a nice color"),
    ("This car is red", "This car is blue")
])
def test_valid_paraphrasing(text1, text2):
    mock_config = Mock(spec=Config)
    mock_config.max_text_similarity = 0.85
    mock_config.min_content_similarity = 0.35
    assert TicketParaphraseValidator(config=mock_config,
                                     similarity_calculator=SimilarityCalculator()).check_pair_is_valid(
        text1, text2)


@pytest.mark.parametrize("text1,text2", [
    ("I like going to school", "My PyCharm IDE is not working correctly. like, going, to"),
    ("These texts are almost completely the same", "These texts are almost completely same"),
    ("This text is exactly the same", "This text is exactly the same")
])
def test_invalid_paraphrasing(text1, text2):
    mock_config = Mock(spec=Config)
    mock_config.max_text_similarity = 0.85
    mock_config.min_content_similarity = 0.35
    assert not TicketParaphraseValidator(config=mock_config,
                                         similarity_calculator=SimilarityCalculator()).check_pair_is_valid(text1, text2)
