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

    try:
        graph.add_node(node)
        assert False
    except ValueError:
        pass