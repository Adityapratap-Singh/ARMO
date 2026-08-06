# Graph Compiler

The graph compiler bridges the planning layer and the execution layer.

## Flow

TaskPlan -> GraphCompiler -> ExecutionGraph

A `TaskPlan` contains a goal plus a list of planning steps. Each step is converted into one execution node. Dependencies from the planning step are used to create directed edges between nodes.

## Responsibilities

- Create one execution node for each planning step.
- Preserve the planning step id as the node id.
- Preserve the planning step description as the node description.
- Create dependency edges using the existing execution graph API.
- Reject invalid plans rather than silently repairing them.

## Validation rules

The compiler raises `ValueError` when:

- a plan contains duplicate node ids
- a dependency refers to a step that does not exist
- the resulting graph contains a cycle

## Example

```python
from armo.graph.compiler import GraphCompiler
from armo.planner.models import PlanningStep, TaskPlan

plan = TaskPlan(
    goal="Build a feature",
    steps=[
        PlanningStep(id="step-1", description="Inspect the code"),
        PlanningStep(id="step-2", description="Implement the feature", depends_on=["step-1"]),
    ],
)

graph = GraphCompiler().compile(plan)
```
