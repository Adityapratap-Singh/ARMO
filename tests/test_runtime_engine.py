import pytest

from armo.contracts.executor import ExecutorContract
from armo.core.events import EventType
from armo.graph.compiler import GraphCompiler
from armo.graph.graph import ExecutionGraph
from armo.graph.node import NodeStatus
from armo.planner.models import PlanningStep, TaskPlan
from armo.runtime.dispatcher import Dispatcher
from armo.runtime.engine import RuntimeEngine
from armo.runtime.worker import Worker


class DummyExecutor(ExecutorContract):
    def __init__(self, outputs: dict[str, str] | None = None, fail_node: str | None = None) -> None:
        self.outputs = outputs or {}
        self.fail_node = fail_node

    def execute(self, task):
        if self.fail_node and task.id == self.fail_node:
            raise RuntimeError("boom")

        return type(
            "Result",
            (),
            {"subtask_id": task.id, "output": self.outputs.get(task.id, "ok"), "confidence": 1.0, "latency": 0.1, "token_cost": 1, "dollar_cost": 0.0, "tool_failures": 0},
        )()


def test_runtime_executes_single_node() -> None:
    graph = ExecutionGraph()
    graph.add_node(type("Node", (), {"id": "step-1", "prompt": "Do it", "status": NodeStatus.PENDING, "mark_running": lambda self: None, "mark_completed": lambda self, result=None: None})())

    engine = RuntimeEngine(executor=DummyExecutor())
    state, history = engine.execute(graph)

    assert history.total_events >= 2
    assert any(event.event == EventType.RUNTIME_FINISHED for event in history.events)


def test_runtime_executes_linear_graph() -> None:
    plan = TaskPlan(
        goal="Linear",
        steps=[
            PlanningStep(id="step-1", description="First"),
            PlanningStep(id="step-2", description="Second", depends_on=["step-1"]),
        ],
    )
    graph = GraphCompiler().compile(plan)

    engine = RuntimeEngine(executor=DummyExecutor())
    state, history = engine.execute(graph)

    assert graph.get_node("step-1").status.name == "COMPLETED"
    assert graph.get_node("step-2").status.name == "COMPLETED"
    assert history.total_events >= 4


def test_runtime_executes_diamond_graph() -> None:
    plan = TaskPlan(
        goal="Diamond",
        steps=[
            PlanningStep(id="step-1", description="Root"),
            PlanningStep(id="step-2", description="Left", depends_on=["step-1"]),
            PlanningStep(id="step-3", description="Right", depends_on=["step-1"]),
            PlanningStep(id="step-4", description="Join", depends_on=["step-2", "step-3"]),
        ],
    )
    graph = GraphCompiler().compile(plan)

    engine = RuntimeEngine(executor=DummyExecutor())
    state, history = engine.execute(graph)

    assert graph.get_node("step-4").status.name == "COMPLETED"
    assert graph.get_node("step-2").status.name == "COMPLETED"
    assert graph.get_node("step-3").status.name == "COMPLETED"


def test_runtime_marks_failed_node_and_stops() -> None:
    plan = TaskPlan(
        goal="Fail",
        steps=[
            PlanningStep(id="step-1", description="Will fail"),
            PlanningStep(id="step-2", description="Never runs", depends_on=["step-1"]),
        ],
    )
    graph = GraphCompiler().compile(plan)

    engine = RuntimeEngine(executor=DummyExecutor(fail_node="step-1"))
    state, history = engine.execute(graph)

    assert graph.get_node("step-1").status.name == "FAILED"
    assert graph.get_node("step-2").status.name == "PENDING"
    assert any(event.event == EventType.RUNTIME_FINISHED for event in history.events)


def test_worker_executes_node() -> None:
    node = type("Node", (), {"id": "step-1", "prompt": "Do it"})()
    worker = Worker(executor=DummyExecutor())

    result = worker.execute(node)

    assert result.subtask_id == "step-1"


def test_dispatcher_returns_first_ready_node() -> None:
    dispatcher = Dispatcher()
    ready = [type("Node", (), {"id": "step-1"})(), type("Node", (), {"id": "step-2"})()]

    node = dispatcher.dispatch(ready)

    assert node is ready[0]
