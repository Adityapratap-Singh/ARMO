from __future__ import annotations

from armo.graph.graph import ExecutionGraph
from armo.graph.node import ExecutionNode
from armo.planner.models import PlanningStep, TaskPlan


class GraphCompiler:
    """Compile a TaskPlan into an ExecutionGraph."""

    def compile(self, plan: TaskPlan) -> ExecutionGraph:
        if not plan.steps:
            return ExecutionGraph()

        self._validate_plan(plan)

        graph = ExecutionGraph()

        for step in plan.steps:
            node = ExecutionNode(
                id=step.id,
                prompt=step.description,
                metadata={"description": step.description},
            )
            graph.add_node(node)

        for step in plan.steps:
            for dependency_id in step.depends_on:
                graph.add_dependency(dependency_id, step.id)

        if graph.has_cycle():
            raise ValueError("Graph contains a cycle")

        return graph

    def _validate_plan(self, plan: TaskPlan) -> None:
        seen_ids: set[str] = set()
        for step in plan.steps:
            if step.id in seen_ids:
                raise ValueError(f"duplicate node id '{step.id}'")
            seen_ids.add(step.id)

        known_ids = {step.id for step in plan.steps}
        for step in plan.steps:
            for dependency_id in step.depends_on:
                if dependency_id == step.id:
                    raise ValueError(
                        f"missing dependency '{dependency_id}' for node '{step.id}'"
                    )
                if dependency_id not in known_ids:
                    raise ValueError(
                        f"missing dependency '{dependency_id}' for node '{step.id}'"
                    )
