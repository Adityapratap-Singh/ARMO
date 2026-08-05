from __future__ import annotations

from abc import ABC, abstractmethod

from armo.models import AgentResult, SubTask


class ExecutorContract(ABC):
    """
    Base contract for every execution backend.
    """

    @abstractmethod
    def execute(
        self,
        task: SubTask,
    ) -> AgentResult:
        """
        Execute a single subtask.

        Returns
        -------
        AgentResult
        """
        raise NotImplementedError