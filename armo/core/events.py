from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, UTC
from enum import Enum

from armo.models import SwitchReason, Topology


class EventType(str, Enum):
    RUNTIME_STARTED = "runtime_started"
    STEP_STARTED = "step_started"
    STEP_COMPLETED = "step_completed"

    TOPOLOGY_SWITCH_REQUESTED = "topology_switch_requested"
    TOPOLOGY_SWITCH_STARTED = "topology_switch_started"
    TOPOLOGY_SWITCH_COMPLETED = "topology_switch_completed"

    TASK_COMPLETED = "task_completed"

    RUNTIME_FINISHED = "runtime_finished"


@dataclass(slots=True)
class RuntimeEvent:
    """
    Immutable runtime event.
    """

    event: EventType

    timestamp: datetime

    message: str

    topology: Topology | None = None

    reason: SwitchReason | None = None

    step: int | None = None

    @staticmethod
    def now(
        event: EventType,
        message: str,
        topology: Topology | None = None,
        reason: SwitchReason | None = None,
        step: int | None = None,
    ) -> "RuntimeEvent":

        return RuntimeEvent(
            event=event,
            timestamp=datetime.now(),
            message=message,
            topology=topology,
            reason=reason,
            step=step,
        )