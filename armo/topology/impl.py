from __future__ import annotations

from armo.core.state import RuntimeState
from armo.graph.graph import ExecutionGraph
from armo.topology.base import BaseTopology


class ChainTopology(BaseTopology):
    name = "chain"

    def transform(self, graph: ExecutionGraph, runtime_state: RuntimeState) -> ExecutionGraph:
        return self._clone_graph(graph)


class ParallelTopology(BaseTopology):
    name = "parallel"

    def transform(self, graph: ExecutionGraph, runtime_state: RuntimeState) -> ExecutionGraph:
        return self._clone_graph(graph)
