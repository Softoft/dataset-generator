import enum
import logging
from enum import Enum

from openai.types.beta.threads import Run


class CostType(Enum):
    INPUT = enum.auto()
    OUTPUT = enum.auto()


def per_million_tokens(cost: float):
    return cost / 10 ** 6


class AssistantRun:
    def __init__(self, run: Run):
        self.run = run

    def calculate_cost(self):
        input_cost = self._get_cost(CostType.INPUT) * self.run.usage.prompt_tokens
        output_cost = self._get_cost(CostType.OUTPUT) * self.run.usage.completion_tokens
        return input_cost + output_cost

    def _get_cost(self, cost_type: CostType):
        cost_map = {
            CostType.INPUT: {
                "gpt-4o": per_million_tokens(5),
                "gpt-4o-mini": per_million_tokens(0.15),
            },
            CostType.OUTPUT: {
                "gpt-4o": per_million_tokens(15),
                "gpt-4o-mini": per_million_tokens(0.6),
            }
        }
        return cost_map[cost_type][self.run.model]


class AssistantAnalyzer:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AssistantAnalyzer, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'runs'):
            self.runs: list[AssistantRun] = []

    def append_run(self, run: Run):
        self.runs.append(AssistantRun(run))
        self._log_run_status(run)

    def calculate_total_cost(self):
        return sum([run.calculate_cost() for run in self.runs])

    def calculate_average_cost(self):
        return self.calculate_total_cost() / len(self.runs)

    def _log_run_status(self, run: Run):
        if run.status != "completed":
            logging.error(f"Run failed with status {run.status} and run {run}")
        if run.usage:
            logging.info(f"Run Usage: {run.usage}")
