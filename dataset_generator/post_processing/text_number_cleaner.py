import random
import re


class TextNumberCleaner:
    def get_possible_decreasing_number_sequences(self, length):
        sequences = []
        for start in range(9, length - 1, -1):
            sequences.append(list(range(start, start - length, -1)))
        return sequences

    def get_possible_increasing_number_sequences(self, length):
        sequences = []
        for start in range(0, 10 - length + 1):
            sequences.append(list(range(start, start + length)))
        return sequences

    def generate_sequential_number_regex(self, length):
        all_sequences = (self.get_possible_decreasing_number_sequences(length)
                         + self.get_possible_increasing_number_sequences(length))

        return "|".join([''.join(map(str, seq)) for seq in all_sequences])

    def random_number(self, length):
        first_digit = random.randint(1, 9)
        return str(first_digit) + ''.join([str(random.randint(0, 9)) for _ in range(length - 1)])

    def is_sequential(self, digits, increasing=True):
        return all(int(b) - int(a) == (1 if increasing else -1) for a, b in zip(digits, digits[1:]))

    def replace_sequence(self, match: re.Match):
        seq = match.group()
        return self.random_number(len(seq))

    def process_text(self, text):
        digit_sequence_regex = self.generate_sequential_number_regex(3)
        processed_text = re.sub(digit_sequence_regex, self.replace_sequence, text)
        return processed_text

    def process_file(self, file_path, save_file_path):
        with open(file_path, encoding="utf-8") as file:
            text = file.read()
        processed_text = self.process_text(text)
        with open(save_file_path, "w", encoding="utf-8") as file:
            file.write(processed_text)
