from __future__ import annotations

import time
from typing import Optional

from armo.contracts.executor import ExecutorContract

from .base import BasePlanner
from .models import PlanningResult
from .parser import PlanningParser
from .prompt_loader import PromptLoader


class LLMPlanner(BasePlanner):
    """Planner backed by a Large Language Model."""

    def __init__(self, executor: Optional[ExecutorContract] = None):
        self.executor = executor

    def plan(self, goal: str) -> PlanningResult:
        """Generate a task plan using an LLM."""

        if self.executor is None:
            raise RuntimeError("Planner requires an executor.")

        system_prompt = PromptLoader.load_system_prompt()
        user_prompt = PromptLoader.load_user_prompt(goal)

        started_at = time.perf_counter()
        raw_response = self.executor.generate(
            system=system_prompt,
            prompt=user_prompt,
        )
        planning_time = time.perf_counter() - started_at

        task_plan = PlanningParser.parse(raw_response)

        return PlanningResult(
            plan=task_plan,
            raw_response=raw_response,
            planner_model=self._planner_model_name(),
            planning_time=planning_time,
        )

    def _planner_model_name(self) -> str:
        if hasattr(self.executor, "model") and self.executor.model:
            return str(self.executor.model)
        return "unknown"