import logging

import pytest

from graph.data.models import Language
from src.util.text_similarity_calculator import compute_text_similarity


def test_returns_correct_similarity_for_identical_texts():
    result = compute_text_similarity("same text", "same text")
    assert pytest.approx(result, 0.01) == 1.0


def test_returns_correct_similarity_for_different_texts():
    result = compute_text_similarity("text one", "text two")
    assert 0.0 < result < 1.0


def test_returns_one_for_empty_texts():
    result = compute_text_similarity("", "")
    assert result == 1.0


def test_returns_zero_for_one_empty_text():
    result = compute_text_similarity("non-empty text", "")
    assert result == 0.0


@pytest.mark.parametrize("similar_text_pair,less_similar_text_pair",
                         [
                             (("I like to go to school", "I like going to my school"), ("My favorite color is blue", "I like to go to school")),
                             (("The quick brown fox jumps over the lazy dog", "A quick brown fox jumps over a lazy dog"), ("The sun is shining brightly", "I love rainy days")),
                             (("She sells seashells by the seashore", "She sells seashells on the seashore"), ("He loves to play football", "She enjoys reading books"))
                         ])
def test_similarity_scores_of_texts(similar_text_pair,less_similar_text_pair):
    similar_text_pair_score = compute_text_similarity(similar_text_pair[0], similar_text_pair[1])

    less_similar_text_pair_score = compute_text_similarity(less_similar_text_pair[0], less_similar_text_pair[1])
    logging.info(f"{similar_text_pair[0]}; {similar_text_pair[1]} => {similar_text_pair_score}")
    logging.info(f"Similarity score of less similar text pair: {less_similar_text_pair_score}")
    assert similar_text_pair_score > less_similar_text_pair_score
