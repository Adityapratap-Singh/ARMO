from __future__ import annotations

from armo.graph.node import ExecutionNode


class Dispatcher:
    """Dispatch ready nodes one at a time for the initial runtime phase."""

    def __init__(self) -> None:
        self._dispatch_count = 0

    def dispatch(self, ready_nodes: list[ExecutionNode]) -> ExecutionNode | None:
        if not ready_nodes:
            return None

        self._dispatch_count += 1
        return ready_nodes[0]
