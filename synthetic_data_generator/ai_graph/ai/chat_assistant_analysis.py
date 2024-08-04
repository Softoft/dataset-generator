import enum
import logging
from enum import Enum
from typing import Dict, List

from openai.types.beta.threads import Run


def cost_analyzer(cls):
    original_init = cls.__init__

    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        original_create_run = self.create_run

        async def wrapped_create_run(*args, **kwargs):
            run = await original_create_run(*args, **kwargs)
            AssistantAnalyzer.get_instance().append_run(run, self.chat_assistant_config.assistant_name)
            return run

        self.create_run = wrapped_create_run

    cls.__init__ = new_init
    return cls


class CostType(Enum):
    INPUT = enum.auto()
    OUTPUT = enum.auto()


def per_million_tokens(cost: float) -> float:
    return cost / 10 ** 6


class AssistantRun:
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

    def __init__(self, run: Run, assistant_name: str):
        self.run = run
        self.assistant_name = assistant_name

    def calculate_cost(self) -> float:
        try:
            input_cost = self.cost_map[CostType.INPUT][self.run.model] * self.run.usage.prompt_tokens
            output_cost = self.cost_map[CostType.OUTPUT][self.run.model] * self.run.usage.completion_tokens
            return input_cost + output_cost
        except KeyError as e:
            logging.error(f"Model {self.run.model} not found in cost map: {e}")
            return 0.0


class AssistantAnalyzer:
    _instance = None

    @classmethod
    def get_instance(cls) -> "AssistantAnalyzer":
        if cls._instance is None:
            cls._instance = AssistantAnalyzer()
        return cls._instance

    def __init__(self):
        self.runs: List[AssistantRun] = []

    def append_run(self, run: Run, assistant_name: str):
        self.runs.append(AssistantRun(run, assistant_name))
        self._log_run_status(run)

    def calculate_total_cost(self) -> float:
        return sum(run.calculate_cost() for run in self.runs)

    def generate_cost_summary(self):
        assistant_name_runs: Dict[str, List[AssistantRun]] = { }
        for run in self.runs:
            assistant_name_runs.setdefault(run.assistant_name, []).append(run)

        summary_lines = []
        total_cost = self.calculate_total_cost()

        for assistant_name, runs in assistant_name_runs.items():
            total_assistant_cost = sum(run.calculate_cost() for run in runs)
            percentage_total_cost = (total_assistant_cost / total_cost) * 100
            prompt_tokens = sum(run.run.usage.prompt_tokens for run in runs)
            completion_tokens = sum(run.run.usage.completion_tokens for run in runs)

            summary_lines.append(
                f"Assistant: {assistant_name}\n"
                f"Total Cost: {round(total_assistant_cost, 3)}€\n"
                f"Percentage of Total Cost: {round(percentage_total_cost, 2)}%\n"
                f"Prompt Tokens: {prompt_tokens:,}\n"
                f"Completion Tokens: {completion_tokens:,}\n"
            )

        logging.warning("\n".join(summary_lines))

    def _log_run_status(self, run: Run):
        if run.status != "completed":
            logging.error(f"Run failed with status {run.status} and run {run}")
        if run.usage:
            logging.info(f"Run Usage: {run.usage}")
