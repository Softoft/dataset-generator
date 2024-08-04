import logging
import re
from collections import Counter
from dataclasses import dataclass

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from graph.data.models import NumberInterval, Ticket


class SimilarityCalculator:
    def get_content_similarity(self, text1: str, text2: str) -> float:
        if text1 == "" and text2 == "":
            return 1.0
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([text1, text2])

        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

        score = similarity[0][0]
        logging.info(f"Content similarity score: {score}")
        return score

    def get_text_similarity(self, text1: str, text2: str):
        wfs = self.__word_frequency_similarity_score(text1, text2)
        lcs = self.__lcs_score(text1, text2)
        score = min(wfs, lcs)
        logging.info(f"Text similarity score: wfs {wfs:.2}, lcs {lcs:.2}:  {score:.2}")
        return score

    def __tokenize(self, text):
        return re.findall(r'\b\w+\b', text)

    def __lcs_length(self, words1, words2):
        m, n = len(words1), len(words2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if words1[i - 1] == words2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        return dp[m][n]

    def __lcs_score(self, text1, text2):
        words1 = self.__tokenize(text1)
        words2 = self.__tokenize(text2)
        lcs_len = self.__lcs_length(words1, words2)
        max_len = max(min(len(words1), len(words2)), 1)
        return 2 ** ((lcs_len - max_len) / 2 ** 2)

    def __word_frequency_similarity_score(self, text1, text2):
        words1 = self.__tokenize(text1)
        words2 = self.__tokenize(text2)
        freq1 = Counter(words1)
        freq2 = Counter(words2)
        differences = [abs(freq1.get(key, 0) - freq2.get(key, 0)) for key in
                       list(freq1.keys()) + list(freq2.keys())]
        word_difference_score = ((sum(differences)) / (len(words1) + len(words2)))
        return max(1 - word_difference_score, 0)


@dataclass
class TicketParaphraseValidator:
    text_similarity_bounds: NumberInterval
    content_similarity_bounds: NumberInterval
    similarity_calculator: SimilarityCalculator

    def check_pair_is_valid(self, text1, text2, empty_allowed=False):
        if empty_allowed and (text1 == "" or text2 == ""):
            return True
        return (self.similarity_calculator.get_text_similarity(text1, text2) in self.text_similarity_bounds and
                self.similarity_calculator.get_content_similarity(text1, text2) in self.content_similarity_bounds)

    def is_valid_paraphrasing(self, ticket1: Ticket, ticket2: Ticket):
        valid_subject = self.check_pair_is_valid(ticket1.subject, ticket2.subject, empty_allowed=True)
        valid_body = self.check_pair_is_valid(ticket1.body, ticket2.body)
        valid_answer = self.check_pair_is_valid(ticket1.answer, ticket2.answer)
        return valid_subject and valid_body and valid_answer
