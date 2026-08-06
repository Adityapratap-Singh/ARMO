from __future__ import annotations

from .base import BasePlanner
from .models import PlanningResult


class LLMPlanner(BasePlanner):
    """
    Planner backed by a Large Language Model.
    """

    def __init__(self, executor):
        self.executor = executor

    def plan(self, goal: str) -> PlanningResult:
        raise NotImplementedError("LLM planning is not implemented yet.")