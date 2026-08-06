from armo.config import ARMOConfig
from armo.core.events import EventType
from armo.core.history import RuntimeHistory
from armo.core.state import RuntimeState
from armo.graph.compiler import GraphCompiler
from armo.planner.models import PlanningStep, TaskPlan
from armo.runtime.engine import RuntimeEngine
from armo.topology.manager import TopologyManager


class DummyExecutor:
    def execute(self, task):
        return type(
            "Result",
            (),
            {
                "subtask_id": task.id,
                "output": "ok",
                "confidence": 0.9,
                "latency": 0.1,
                "token_cost": 1,
                "dollar_cost": 0.0,
                "tool_failures": 0,
            },
        )()


def test_runtime_invokes_topology_manager_and_records_events() -> None:
    plan = TaskPlan(
        goal="Switching",
        steps=[
            PlanningStep(id="step-1", description="First"),
            PlanningStep(id="step-2", description="Second", depends_on=["step-1"]),
        ],
    )
    graph = GraphCompiler().compile(plan)

    manager = TopologyManager()
    engine = RuntimeEngine(executor=DummyExecutor(), config=ARMOConfig(), topology_manager=manager)
    state, history = engine.execute(graph)

    assert state.switch_count >= 0
    assert any(event.event == EventType.TOPOLOGY_SWITCH_REQUESTED for event in history.events)
    assert any(event.event == EventType.TOPOLOGY_SWITCH_COMPLETED for event in history.events)
