from armo.config import ARMOConfig
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


if __name__ == "__main__":
    plan = TaskPlan(
        goal="Topology Demo",
        steps=[
            PlanningStep(id="step-1", description="First"),
            PlanningStep(id="step-2", description="Second", depends_on=["step-1"]),
        ],
    )
    graph = GraphCompiler().compile(plan)
    manager = TopologyManager()
    engine = RuntimeEngine(executor=DummyExecutor(), config=ARMOConfig(), topology_manager=manager)
    state, history = engine.execute(graph)

    print("Current Topology")
    print("↓")
    print(f"Switch Decision: {state.current_topology}")
    print("↓")
    print("Topology Manager")
    print("↓")
    print(f"New Topology: {state.current_topology}")
    print("↓")
    print("Execution Continues")
