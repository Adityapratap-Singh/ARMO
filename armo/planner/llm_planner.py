from __future__ import annotations

from typing import Optional

from armo.contracts.executor import ExecutorContract

from .base import BasePlanner
from .models import PlanningResult


class LLMPlanner(BasePlanner):
    """
    Planner backed by a Large Language Model.
    """

    def __init__(self, executor: Optional[ExecutorContract] = None):
        self.executor = executor

    def plan(self, goal: str) -> PlanningResult:
        """
        Generate a task plan using an LLM.
        """
        raise NotImplementedError("LLM planning is not implemented yet.")