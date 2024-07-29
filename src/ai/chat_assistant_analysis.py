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
    def __init__(self, run: Run, assistant_name: str):
        self.run = run
        self.assistant_name = assistant_name

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

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = AssistantAnalyzer()
        return cls._instance

    def __init__(self):
        self.runs: list[AssistantRun] = []

    def append_run(self, run: Run, assistant_name: str):
        self.runs.append(AssistantRun(run, assistant_name))
        self._log_run_status(run)

    def calculate_total_cost(self):
        return sum([run.calculate_cost() for run in self.runs])

    def generate_cost_summary(self):
        assistant_name_runs = {}
        for run in self.runs:
            if run.assistant_name not in assistant_name_runs:
                assistant_name_runs[run.assistant_name] = []
            assistant_name_runs[run.assistant_name].append(run)

        summary_string = ""
        for assistant_name, runs in assistant_name_runs.items():
            summary_string += f"Assistant: {assistant_name}\n Total Cost: {round(sum([run.calculate_cost() for run in runs]), 3)}€ " +\
                              f"Prompt Tokens: {sum([run.run.usage.prompt_tokens for run in runs]):,}" + \
                              f"Completion Tokens: {sum([run.run.usage.completion_tokens for run in runs]):,}\n"
        logging.warning(summary_string)

    def _log_run_status(self, run: Run):
        if run.status != "completed":
            logging.error(f"Run failed with status {run.status} and run {run}")
        if run.usage:
            logging.info(f"Run Usage: {run.usage}")
