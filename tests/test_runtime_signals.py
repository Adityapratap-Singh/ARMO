from armo.config import ARMOConfig
from armo.core.events import EventType
from armo.core.signal_engine import SignalEngine
from armo.core.switching import SwitchingDecision, SwitchingPolicy
from armo.graph.compiler import GraphCompiler
from armo.graph.node import NodeStatus
from armo.planner.models import PlanningStep, TaskPlan
from armo.runtime.engine import RuntimeEngine


class DummyExecutor:
    def __init__(self, outputs: dict[str, str] | None = None) -> None:
        self.outputs = outputs or {}

    def execute(self, task):
        return type(
            "Result",
            (),
            {
                "subtask_id": task.id,
                "output": self.outputs.get(task.id, "ok"),
                "confidence": 0.9,
                "latency": 0.1,
                "token_cost": 1,
                "dollar_cost": 0.0,
                "tool_failures": 0,
            },
        )()


def test_runtime_generates_signals_after_each_completed_node() -> None:
    plan = TaskPlan(
        goal="Signals",
        steps=[
            PlanningStep(id="step-1", description="First"),
            PlanningStep(id="step-2", description="Second", depends_on=["step-1"]),
        ],
    )
    graph = GraphCompiler().compile(plan)

    engine = RuntimeEngine(executor=DummyExecutor())
    state, history = engine.execute(graph)

    completed_events = [
        event for event in history.events if event.message.startswith("Completed node")
    ]

    assert len(completed_events) == 2
    assert any("signal" in event.message.lower() for event in history.events)
    assert any("switching" in event.message.lower() for event in history.events)


def test_switching_policy_invoked_once_per_completed_node() -> None:
    plan = TaskPlan(
        goal="Signals",
        steps=[
            PlanningStep(id="step-1", description="First"),
            PlanningStep(id="step-2", description="Second", depends_on=["step-1"]),
        ],
    )
    graph = GraphCompiler().compile(plan)

    engine = RuntimeEngine(executor=DummyExecutor())
    state, history = engine.execute(graph)

    switching_events = [
        event for event in history.events if "switching decision" in event.message.lower()
    ]

    assert len(switching_events) == 2


def test_signal_engine_and_policy_are_used_for_feedback_loop() -> None:
    signals = SignalEngine.compute(
        completed_results=[
            type(
                "Result",
                (),
                {"confidence": 0.80, "latency": 0.1, "tool_failures": 0},
            )()
        ],
        remaining_subtasks=[type("SubTask", (), {"difficulty": 0.6, "dependencies": []})()],
        coupling=0.5,
    )

    policy = SwitchingPolicy(ARMOConfig())
    decision = policy.evaluate(signals)

    assert isinstance(decision, SwitchingDecision)
    assert decision.topology is None or decision.reason in {None, type(decision.reason).__members__["NONE"]}
