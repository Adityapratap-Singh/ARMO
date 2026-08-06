from armo.core.state import RuntimeState
from armo.graph.graph import ExecutionGraph
from armo.graph.node import ExecutionNode
from armo.models import TaskProfile, TaskType, Topology, SwitchReason
from armo.topology.manager import TopologyManager
from armo.topology.types import TopologyType


def test_manager_applies_switching_decision_and_updates_state() -> None:
    graph = ExecutionGraph()
    graph.add_node(ExecutionNode(id="step-1", prompt="Do it"))

    state = RuntimeState(task=TaskProfile(id="task", description="demo", task_type=TaskType.REASONING, subtasks=[], parallelism_width=0.0, coupling_density=0.0, critical_path_depth=1))
    manager = TopologyManager()

    decision = type("Decision", (), {"topology": Topology.PARALLEL, "reason": SwitchReason.PARALLELISM})()
    transformed_graph = manager.apply_decision(graph, state, decision)

    assert transformed_graph is not None
    assert transformed_graph is not graph
    assert state.current_topology == Topology.PARALLEL
    assert state.switch_count == 1
    assert state.last_switch_reason == SwitchReason.PARALLELISM
