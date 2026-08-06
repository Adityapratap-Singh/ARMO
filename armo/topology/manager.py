from __future__ import annotations

from armo.core.events import EventType, RuntimeEvent
from armo.core.history import RuntimeHistory
from armo.core.state import RuntimeState
from armo.core.switching import SwitchingDecision
from armo.graph.graph import ExecutionGraph
from armo.models import Topology, SwitchReason
from armo.topology.factory import TopologyFactory
from armo.topology.types import TopologyType


class TopologyManager:
    """Coordinate runtime topology switching without changing graph semantics yet."""

    def __init__(self, factory: TopologyFactory | None = None) -> None:
        self.factory = factory or TopologyFactory()

    def apply_decision(
        self,
        graph: ExecutionGraph,
        runtime_state: RuntimeState,
        decision: SwitchingDecision,
    ) -> ExecutionGraph:
        if decision.topology is None:
            return graph

        runtime_state.previous_topology = runtime_state.current_topology
        runtime_state.current_topology = decision.topology
        runtime_state.switch_count += 1
        runtime_state.last_switch_reason = decision.reason

        topology_type = self._to_topology_type(decision.topology)
        topology = self.factory.create(topology_type)
        transformed_graph = topology.transform(graph, runtime_state) if topology is not None else graph
        return transformed_graph

    def record_history(self, history: RuntimeHistory, previous: Topology | None, new: Topology, reason: SwitchReason) -> None:
        history.add(
            RuntimeEvent.now(
                EventType.TOPOLOGY_SWITCH_COMPLETED,
                f"Topology switched from {previous} to {new} ({reason.value})",
                topology=new,
                reason=reason,
            )
        )

    def _to_topology_type(self, topology: Topology) -> TopologyType:
        mapping = {
            Topology.PARALLEL: TopologyType.PARALLEL,
            Topology.SEQUENTIAL: TopologyType.CHAIN,
            Topology.ROUTING: TopologyType.CHAIN,
            Topology.EVALUATOR_OPTIMIZER: TopologyType.EVALUATOR_OPTIMIZER,
            Topology.PLANNER_WORKER: TopologyType.CHAIN,
        }
        return mapping.get(topology, TopologyType.CHAIN)
