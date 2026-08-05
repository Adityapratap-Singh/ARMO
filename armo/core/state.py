from __future__ import annotations

from dataclasses import dataclass, field

from armo.models import (
    AgentResult,
    RuntimeSignals,
    SubTask,
    TaskProfile,
    Topology,
    SwitchReason,
)


@dataclass
class RuntimeState:
    """
    Central mutable state for one ARMO execution.

    Every runtime component reads from this object.
    The Runtime Engine is responsible for updating it.
    """

    # Input
    task: TaskProfile

    # Task progress
    pending: list[SubTask] = field(default_factory=list)
    completed: list[SubTask] = field(default_factory=list)
    results: list[AgentResult] = field(default_factory=list)

    # Topology
    current_topology: Topology = Topology.PLANNER_WORKER
    previous_topology: Topology | None = None

    # Switching
    switch_count: int = 0
    persistence_counter: int = 0
    last_switch_reason: SwitchReason = SwitchReason.NONE

    # Metrics
    total_latency: float = 0.0
    total_tokens: int = 0
    total_cost: float = 0.0

    # Signals
    signals: RuntimeSignals | None = None

    # Execution
    step: int = 0

    def __post_init__(self) -> None:
        if not self.pending:
            self.pending = list(self.task.subtasks)

    @property
    def finished(self) -> bool:
        return len(self.pending) == 0

    def record_result(self, result: AgentResult) -> None:
        self.results.append(result)
        self.total_latency += result.latency
        self.total_tokens += result.token_cost
        self.total_cost += result.dollar_cost