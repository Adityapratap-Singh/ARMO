from __future__ import annotations

from abc import ABC, abstractmethod

from armo.core.state import RuntimeState


class TopologyContract(ABC):
    """
    Base class for every orchestration topology.
    """

    @abstractmethod
    def select_tasks(
        self,
        runtime: RuntimeState,
    ):
        raise NotImplementedError