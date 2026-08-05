from __future__ import annotations

from collections import defaultdict

from .node import ExecutionNode


class ExecutionGraph:
    """
    Directed Acyclic Graph (DAG) representing an execution plan.

    The graph stores execution nodes and their dependencies.
    Scheduling and execution are handled by the runtime.
    """

    def __init__(self) -> None:
        self._nodes: dict[str, ExecutionNode] = {}

        # parent -> children
        self._edges: dict[str, set[str]] = defaultdict(set)

        # child -> parents
        self._reverse_edges: dict[str, set[str]] = defaultdict(set)

    # --------------------------------------------------

    def add_node(self, node: ExecutionNode) -> None:
        """Add a node to the graph."""

        if node.id in self._nodes:
            raise ValueError(f"Node '{node.id}' already exists.")

        self._nodes[node.id] = node

    # --------------------------------------------------

    def has_node(self, node_id: str) -> bool:
        return node_id in self._nodes

    # --------------------------------------------------

    def get_node(self, node_id: str) -> ExecutionNode:
        return self._nodes[node_id]

    # --------------------------------------------------

    @property
    def nodes(self) -> dict[str, ExecutionNode]:
        return self._nodes.copy()

    # --------------------------------------------------

    def __len__(self) -> int:
        return len(self._nodes)

    # --------------------------------------------------

    def __contains__(self, node_id: str) -> bool:
        return node_id in self._nodes

    # --------------------------------------------------

    def __repr__(self) -> str:
        return f"ExecutionGraph(nodes={len(self)})"