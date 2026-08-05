
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any


class NodeStatus(str, Enum):
    """Execution lifecycle of a graph node."""

    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass(slots=True)
class ExecutionNode:
    """
    A runtime execution node.

    Represents one executable unit inside an ExecutionGraph.
    """

    id: str

    prompt: str

    capability: str = "general"

    model_tier: str = "strong"

    status: NodeStatus = NodeStatus.PENDING

    retries: int = 0

    max_retries: int = 2

    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    started_at: datetime | None = None

    finished_at: datetime | None = None

    result: Any = None

    metadata: dict[str, Any] = field(default_factory=dict)

    dependencies: set[str] = field(default_factory=set)

    dependents: set[str] = field(default_factory=set)

    # -------------------------------------------------

    def mark_ready(self) -> None:
        self.status = NodeStatus.READY

    def mark_running(self) -> None:
        self.status = NodeStatus.RUNNING
        self.started_at = datetime.now(UTC)

    def mark_completed(self, result: Any = None) -> None:
        self.status = NodeStatus.COMPLETED
        self.finished_at = datetime.now(UTC)
        self.result = result

    def mark_failed(self) -> None:
        self.status = NodeStatus.FAILED
        self.finished_at = datetime.now(UTC)

    @property
    def is_finished(self) -> bool:
        return self.status in (
            NodeStatus.COMPLETED,
            NodeStatus.FAILED,
            NodeStatus.SKIPPED,
        )

    def can_retry(self) -> bool:
        return self.retries < self.max_retries

    def retry(self) -> None:
        self.retries += 1
        self.status = NodeStatus.PENDING

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "prompt": self.prompt,
            "status": self.status.value,
            "dependencies": sorted(self.dependencies),
            "dependents": sorted(self.dependents),
            "retries": self.retries,
            "metadata": self.metadata,
        }