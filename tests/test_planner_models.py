from armo.planner.models import PlanningResult, PlanningStep, TaskPlan


def test_planning_step_contains_metadata() -> None:
    step = PlanningStep(
        id="step-1",
        description="Analyze the request",
        depends_on=["step-0"],
    )

    assert step.id == "step-1"
    assert step.description == "Analyze the request"
    assert step.depends_on == ["step-0"]


def test_task_plan_add_step_and_properties() -> None:
    plan = TaskPlan(goal="Build a planner")
    assert plan.is_empty
    assert plan.step_count == 0

    step = PlanningStep(id="step-1", description="Create models")
    plan.add_step(step)

    assert not plan.is_empty
    assert plan.step_count == 1
    assert plan.steps[0] is step


def test_planning_result_contains_plan_and_metadata() -> None:
    plan = TaskPlan(goal="Create a task plan")
    result = PlanningResult(
        plan=plan,
        raw_response='{"goal": "Create a task plan"}',
        planner_model="qwen2.5-coder",
        planning_time=1.23,
    )

    assert result.plan is plan
    assert result.raw_response.startswith("{")
    assert result.planner_model == "qwen2.5-coder"
    assert result.planning_time == 1.23
