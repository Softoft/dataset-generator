import asyncio

from dataset_generator.color_logging import init_logging
from dataset_generator.dataset_generation import DatasetGenerator

if __name__ == '__main__':
    init_logging()
    asyncio.run(DatasetGenerator(8_400, "../data/training/gpt-4-multi-lang-big-8k-15-07.json",
                                 text_length_mean=251, batch_size=100).generate_dataset())
