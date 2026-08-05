import pytest

from armo.graph import ExecutionGraph, ExecutionNode, NodeStatus


def test_node_creation():
    node = ExecutionNode(
        id="A",
        prompt="Say hello",
    )

    assert node.id == "A"

    assert node.status == NodeStatus.PENDING

    assert node.dependencies == set()

    assert node.dependents == set()

    assert node.retries == 0


def test_node_lifecycle():

    node = ExecutionNode(
        id="B",
        prompt="Test",
    )

    node.mark_ready()

    assert node.status == NodeStatus.READY

    node.mark_running()

    assert node.status == NodeStatus.RUNNING

    node.mark_completed("done")

    assert node.status == NodeStatus.COMPLETED

    assert node.result == "done"


def test_graph_creation():
    graph = ExecutionGraph()

    assert len(graph) == 0


def test_add_node():
    graph = ExecutionGraph()

    node = ExecutionNode(
        id="A",
        prompt="Hello",
    )

    graph.add_node(node)

    assert graph.has_node("A")

    assert len(graph) == 1


def test_duplicate_node():
    graph = ExecutionGraph()

    node = ExecutionNode(
        id="A",
        prompt="Hello",
    )

    graph.add_node(node)

    with pytest.raises(ValueError):
        graph.add_node(node)

def test_ready_nodes_single():
    graph = ExecutionGraph()

    node = ExecutionNode(
        id="A",
        prompt="Task A",
    )

    graph.add_node(node)

    ready = graph.ready_nodes()

    assert len(ready) == 1
    assert ready[0].id == "A"


def test_mark_completed():
    graph = ExecutionGraph()

    node = ExecutionNode(
        id="A",
        prompt="Task",
    )

    graph.add_node(node)

    graph.mark_completed("A")

    assert len(graph.completed_nodes()) == 1

    assert graph.completed_nodes()[0].id == "A"

    assert len(graph.pending_nodes()) == 0


def test_topological_sort_single():
    graph = ExecutionGraph()

    node = ExecutionNode(
        id="A",
        prompt="Task",
    )

    graph.add_node(node)

    order = graph.topological_sort()

    assert len(order) == 1
    assert order[0].id == "A"


def test_cycle_detection_empty():
    graph = ExecutionGraph()

    assert graph.has_cycle() is False

def test_add_dependency():
    graph = ExecutionGraph()

    a = ExecutionNode(id="A", prompt="A")
    b = ExecutionNode(id="B", prompt="B")

    graph.add_node(a)
    graph.add_node(b)

    graph.add_dependency("A", "B")

    assert graph.children("A") == {"B"}
    assert graph.parents("B") == {"A"}


def test_indegree_outdegree():
    graph = ExecutionGraph()

    a = ExecutionNode(id="A", prompt="A")
    b = ExecutionNode(id="B", prompt="B")
    c = ExecutionNode(id="C", prompt="C")

    graph.add_node(a)
    graph.add_node(b)
    graph.add_node(c)

    graph.add_dependency("A", "B")
    graph.add_dependency("A", "C")

    assert graph.outdegree("A") == 2
    assert graph.indegree("B") == 1
    assert graph.indegree("C") == 1


def test_ready_after_dependency_completion():
    graph = ExecutionGraph()

    a = ExecutionNode(id="A", prompt="A")
    b = ExecutionNode(id="B", prompt="B")

    graph.add_node(a)
    graph.add_node(b)

    graph.add_dependency("A", "B")

    ready = graph.ready_nodes()

    assert len(ready) == 1
    assert ready[0].id == "A"

    graph.mark_completed("A")

    ready = graph.ready_nodes()

    assert len(ready) == 1
    assert ready[0].id == "B"