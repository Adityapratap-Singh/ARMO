import pytest

from armo.graph.compiler import GraphCompiler
from armo.graph.graph import ExecutionGraph
from armo.planner.models import PlanningStep, TaskPlan


def test_compile_single_node() -> None:
    plan = TaskPlan(
        goal="Do one thing",
        steps=[PlanningStep(id="step-1", description="Perform the task")],
    )

    graph = GraphCompiler().compile(plan)

    assert isinstance(graph, ExecutionGraph)
    assert len(graph) == 1
    node = graph.get_node("step-1")
    assert node.id == "step-1"
    assert node.description == "Perform the task"


def test_compile_linear_chain() -> None:
    plan = TaskPlan(
        goal="Linear work",
        steps=[
            PlanningStep(id="step-1", description="First step"),
            PlanningStep(id="step-2", description="Second step", depends_on=["step-1"]),
            PlanningStep(id="step-3", description="Third step", depends_on=["step-2"]),
        ],
    )

    graph = GraphCompiler().compile(plan)

    assert graph.parents("step-2") == {"step-1"}
    assert graph.parents("step-3") == {"step-2"}
    assert graph.children("step-1") == {"step-2"}


def test_compile_diamond_graph() -> None:
    plan = TaskPlan(
        goal="Diamond work",
        steps=[
            PlanningStep(id="step-1", description="Root"),
            PlanningStep(id="step-2", description="Branch one", depends_on=["step-1"]),
            PlanningStep(id="step-3", description="Branch two", depends_on=["step-1"]),
            PlanningStep(id="step-4", description="Join", depends_on=["step-2", "step-3"]),
        ],
    )

    graph = GraphCompiler().compile(plan)

    order = [node.id for node in graph.topological_sort()]

    assert graph.parents("step-4") == {"step-2", "step-3"}
    assert order.index("step-2") < order.index("step-4")
    assert order.index("step-3") < order.index("step-4")


@pytest.mark.parametrize("depends_on", [["missing-step"], ["step-2"]])
def test_compile_raises_for_missing_dependency(depends_on: list[str]) -> None:
    plan = TaskPlan(
        goal="Broken plan",
        steps=[
            PlanningStep(id="step-1", description="Root"),
            PlanningStep(id="step-2", description="Child", depends_on=depends_on),
        ],
    )

    with pytest.raises(ValueError, match="missing"):
        GraphCompiler().compile(plan)


def test_compile_raises_for_duplicate_ids() -> None:
    plan = TaskPlan(
        goal="Duplicate plan",
        steps=[
            PlanningStep(id="step-1", description="First"),
            PlanningStep(id="step-1", description="Second"),
        ],
    )

    with pytest.raises(ValueError, match="duplicate"):
        GraphCompiler().compile(plan)


def test_compile_empty_plan() -> None:
    plan = TaskPlan(goal="Empty plan")

    graph = GraphCompiler().compile(plan)

    assert len(graph) == 0
