from __future__ import annotations

from collections import defaultdict, deque

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

        # --------------------------------------------------
    # Execution State
    # --------------------------------------------------

    def ready_nodes(self) -> list[ExecutionNode]:
        """
        Return all nodes that are ready for execution.

        A node is ready when:
        - status == PENDING
        - all parent nodes are COMPLETED
        """

        ready: list[ExecutionNode] = []

        for node_id, node in self._nodes.items():

            if node.status.name != "PENDING":
                continue

            parents = self._reverse_edges[node_id]

            if all(
                self._nodes[parent].status.name == "COMPLETED"
                for parent in parents
            ):
                ready.append(node)

        return ready

    # --------------------------------------------------

    def mark_completed(self, node_id: str, result=None) -> None:
        """
        Mark a node as completed.
        """

        self._nodes[node_id].mark_completed(result)

    # --------------------------------------------------

    def mark_failed(self, node_id: str) -> None:
        """
        Mark a node as failed.
        """

        self._nodes[node_id].mark_failed()

    # --------------------------------------------------

    def completed_nodes(self) -> list[ExecutionNode]:

        return [
            node
            for node in self._nodes.values()
            if node.status.name == "COMPLETED"
        ]

    # --------------------------------------------------

    def pending_nodes(self) -> list[ExecutionNode]:

        return [
            node
            for node in self._nodes.values()
            if node.status.name == "PENDING"
        ]

        # --------------------------------------------------
    # Graph Algorithms
    # --------------------------------------------------

    def topological_sort(self) -> list[ExecutionNode]:
        """
        Return nodes in topological order using Kahn's algorithm.
        """

        indegree = {
            node_id: len(self._reverse_edges[node_id])
            for node_id in self._nodes
        }

        queue = deque(
            node_id
            for node_id, degree in indegree.items()
            if degree == 0
        )

        result = []

        while queue:
            current = queue.popleft()

            result.append(self._nodes[current])

            for child in self._edges[current]:
                indegree[child] -= 1

                if indegree[child] == 0:
                    queue.append(child)

        if len(result) != len(self._nodes):
            raise ValueError("Graph contains a cycle.")

        return result

    # --------------------------------------------------

    def has_cycle(self) -> bool:
        """
        Return True if the graph contains a cycle.
        """

        try:
            self.topological_sort()
            return False
        except ValueError:
            return True