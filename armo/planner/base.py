from __future__ import annotations

from abc import ABC, abstractmethod

from .models import PlanningResult


class BasePlanner(ABC):
    """
    Abstract interface for all planners.
    """

    @abstractmethod
    def plan(self, goal: str) -> PlanningResult:
        """
        Generate an execution plan for the given goal.
        """
        raise NotImplementedError