from __future__ import annotations

from abc import ABC, abstractmethod

from armo.core.state import RuntimeState
from armo.graph.graph import ExecutionGraph
from armo.graph.node import ExecutionNode


class BaseTopology(ABC):
    """Abstract interface for a runtime topology transformation."""

    name: str = "base"

    @abstractmethod
    def transform(
        self,
        graph: ExecutionGraph,
        runtime_state: RuntimeState,
    ) -> ExecutionGraph:
        """Return a transformed graph for the current runtime state."""
        raise NotImplementedError

    def _clone_graph(self, graph: ExecutionGraph) -> ExecutionGraph:
        cloned_graph = ExecutionGraph()
        for node_id, node in graph.nodes.items():
            cloned_node = ExecutionNode(
                id=node.id,
                prompt=node.prompt,
                capability=getattr(node, "capability", "general"),
                model_tier=getattr(node, "model_tier", "strong"),
                status=getattr(node, "status", None),
                retries=getattr(node, "retries", 0),
                max_retries=getattr(node, "max_retries", 2),
                created_at=getattr(node, "created_at", None),
                started_at=getattr(node, "started_at", None),
                finished_at=getattr(node, "finished_at", None),
                result=getattr(node, "result", None),
                metadata=dict(getattr(node, "metadata", {}) or {}),
                dependencies=set(getattr(node, "dependencies", set())),
                dependents=set(getattr(node, "dependents", set())),
            )
            cloned_graph.add_node(cloned_node)

        for node_id in graph.nodes:
            for child_id in graph.children(node_id):
                cloned_graph.add_dependency(node_id, child_id)

        return cloned_graph
