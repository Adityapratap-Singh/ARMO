from __future__ import annotations

from dataclasses import dataclass, field

from armo.core.events import RuntimeEvent


@dataclass(slots=True)
class RuntimeHistory:
    """
    Stores all runtime events for a single execution.
    """

    events: list[RuntimeEvent] = field(default_factory=list)

    def add(self, event: RuntimeEvent) -> None:
        self.events.append(event)

    def clear(self) -> None:
        self.events.clear()

    @property
    def total_events(self) -> int:
        return len(self.events)

    def __iter__(self):
        return iter(self.events)