import asyncio

from src.dataset_generation import DatasetGeneratorBuilder
from util.color_logging import init_logging

if __name__ == '__main__':
    init_logging()
    dataset_generator_builder = DatasetGeneratorBuilder(400, "../data/training/gpt-4-multi-lang-big-1k-randomized.json",
                                                        100)
    dataset_generator_builder.text_length_mean = 250
    dataset_generator_builder.text_length_stddev_factor = 2

    asyncio.run(dataset_generator_builder.build().generate_dataset())
