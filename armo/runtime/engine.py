from __future__ import annotations

from armo.config import ARMOConfig
from armo.contracts.executor import ExecutorContract
from armo.core.events import EventType, RuntimeEvent
from armo.core.history import RuntimeHistory
from armo.core.signal_engine import SignalEngine
from armo.core.state import RuntimeState
from armo.core.switching import SwitchingPolicy
from armo.graph.graph import ExecutionGraph
from armo.graph.node import ExecutionNode, NodeStatus
from armo.models import Capability, SubTask, TaskProfile, TaskType, Topology
from armo.topology.manager import TopologyManager

from .dispatcher import Dispatcher
from .worker import Worker


class RuntimeEngine:
    """Execute an ExecutionGraph sequentially using reusable runtime components."""

    def __init__(
        self,
        executor: ExecutorContract,
        dispatcher: Dispatcher | None = None,
        worker: Worker | None = None,
        config: ARMOConfig | None = None,
        topology_manager: TopologyManager | None = None,
    ) -> None:
        self.executor = executor
        self.dispatcher = dispatcher or Dispatcher()
        self.worker = worker or Worker(executor)
        self.config = config or ARMOConfig()
        self.switching_policy = SwitchingPolicy(self.config)
        self.topology_manager = topology_manager or TopologyManager()

    def execute(self, graph: ExecutionGraph) -> tuple[RuntimeState, RuntimeHistory]:
        state = RuntimeState(
            task=TaskProfile(
                id="runtime-task",
                description="Execution graph runtime",
                task_type=TaskType.REASONING,
                subtasks=[
                    SubTask(
                        id=node_id,
                        description=node.prompt,
                        capability=Capability.GENERAL,
                        difficulty=0.0,
                        dependencies=[],
                    )
                    for node_id, node in graph.nodes.items()
                ],
                parallelism_width=0.0,
                coupling_density=0.0,
                critical_path_depth=max(1, len(graph.nodes)),
            )
        )
        history = RuntimeHistory()
        root_graph = graph

        history.add(
            RuntimeEvent.now(
                EventType.RUNTIME_STARTED,
                "Runtime execution started",
                topology=Topology.PLANNER_WORKER,
            )
        )

        while not self._graph_finished(graph):
            ready_nodes = graph.ready_nodes()
            if not ready_nodes:
                break

            node = self.dispatcher.dispatch(ready_nodes)
            if node is None:
                break

            node.mark_running()
            self._mirror_node_state(root_graph, node, "running")
            history.add(
                RuntimeEvent.now(
                    EventType.STEP_STARTED,
                    f"Started node '{node.id}'",
                    topology=Topology.PLANNER_WORKER,
                    step=0,
                )
            )

            try:
                result = self.worker.execute(node)
            except Exception:
                node.mark_failed()
                self._mirror_node_state(root_graph, node, "failed")
                history.add(
                    RuntimeEvent.now(
                        EventType.STEP_COMPLETED,
                        f"Failed node '{node.id}'",
                        topology=Topology.PLANNER_WORKER,
                        step=0,
                    )
                )
                history.add(
                    RuntimeEvent.now(
                        EventType.RUNTIME_FINISHED,
                        "Runtime execution failed",
                        topology=Topology.PLANNER_WORKER,
                    )
                )
                state.step += 1
                return state, history

            node.mark_completed(result)
            self._mirror_node_state(root_graph, node, "completed", result)
            history.add(
                RuntimeEvent.now(
                    EventType.STEP_COMPLETED,
                    f"Completed node '{node.id}'",
                    topology=Topology.PLANNER_WORKER,
                    step=0,
                )
            )

            signals = SignalEngine.compute(
                completed_results=[self._to_agent_result(result)],
                remaining_subtasks=[
                    SubTask(
                        id=remaining_node.id,
                        description=remaining_node.prompt,
                        capability=Capability.GENERAL,
                        difficulty=0.0,
                        dependencies=[],
                    )
                    for remaining_node in graph.pending_nodes()
                ],
                coupling=0.0,
            )
            history.add(
                RuntimeEvent.now(
                    EventType.STEP_COMPLETED,
                    f"Generated signals for node '{node.id}'",
                    topology=Topology.PLANNER_WORKER,
                    step=0,
                )
            )

            decision = self.switching_policy.evaluate(signals)
            history.add(
                RuntimeEvent.now(
                    EventType.STEP_COMPLETED,
                    f"Switching decision evaluated for node '{node.id}': {decision}",
                    topology=Topology.PLANNER_WORKER,
                    step=0,
                )
            )

            if decision.topology is not None:
                history.add(
                    RuntimeEvent.now(
                        EventType.TOPOLOGY_SWITCH_REQUESTED,
                        f"Topology switch requested for node '{node.id}'",
                        topology=decision.topology,
                        reason=decision.reason,
                        step=0,
                    )
                )
                history.add(
                    RuntimeEvent.now(
                        EventType.TOPOLOGY_SWITCH_STARTED,
                        f"Topology switch started for node '{node.id}'",
                        topology=decision.topology,
                        reason=decision.reason,
                        step=0,
                    )
                )
                graph = self.topology_manager.apply_decision(graph, state, decision)
                self.topology_manager.record_history(history, state.previous_topology, state.current_topology, state.last_switch_reason)
                history.add(
                    RuntimeEvent.now(
                        EventType.TOPOLOGY_SWITCH_COMPLETED,
                        f"Topology switch completed for node '{node.id}'",
                        topology=state.current_topology,
                        reason=state.last_switch_reason,
                        step=0,
                    )
                )

            state.step += 1

        history.add(
            RuntimeEvent.now(
                EventType.RUNTIME_FINISHED,
                "Runtime execution completed",
                topology=Topology.PLANNER_WORKER,
            )
        )

        return state, history

    def _graph_finished(self, graph: ExecutionGraph) -> bool:
        return all(node.status.name in {"COMPLETED", "FAILED"} for node in graph.nodes.values())

    def _mirror_node_state(self, graph: ExecutionGraph, node: ExecutionNode, state: str, result: object | None = None) -> None:
        if graph is None:
            return

        mirrored = graph.nodes.get(node.id)
        if mirrored is None:
            return

        if state == "running":
            mirrored.mark_running()
        elif state == "completed":
            mirrored.mark_completed(result)
        elif state == "failed":
            mirrored.mark_failed()

    def _to_agent_result(self, result: object):
        if hasattr(result, "confidence") and hasattr(result, "latency") and hasattr(result, "tool_failures"):
            return result

        return type(
            "AgentResult",
            (),
            {
                "confidence": 1.0,
                "latency": 0.0,
                "tool_failures": 0,
            },
        )()
