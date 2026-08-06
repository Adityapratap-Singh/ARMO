from __future__ import annotations

from armo.contracts.executor import ExecutorContract
from armo.graph.node import ExecutionNode


class Worker:
    """Execute a single graph node via an executor backend."""

    def __init__(self, executor: ExecutorContract) -> None:
        self.executor = executor

    def execute(self, node: ExecutionNode):
        """Run one node through the configured executor."""

        return self.executor.execute(node)
