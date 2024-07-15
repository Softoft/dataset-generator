import logging
import shutil

from text_number_cleaner import TextNumberCleaner


class TicketPostProcessing:
    def __init__(self, load_file_path, save_file_path):
        self.save_file_path = save_file_path
        self.text_cleaner = TextNumberCleaner()
        shutil.copyfile(load_file_path, save_file_path)

    def process_tickets(self):
        self.text_cleaner.process_file(self.save_file_path, self.save_file_path)


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    cleaner = TicketPostProcessing("../data/gpt-4-1k.json",
                                   "../data/gpt-4-3k-clean2.json",
                                   )
    cleaner.process_tickets()
