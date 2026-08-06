import pytest

from armo.planner import LLMPlanner, PlanningResult


class DummyExecutor:
    def __init__(self, response: str, model: str = "mock-model") -> None:
        self._response = response
        self.model = model

    def generate(self, system: str, prompt: str) -> str:
        return self._response


def test_llm_planner_builds_plan_from_executor_response() -> None:
    executor = DummyExecutor(
        '{"goal": "Build a planner", "steps": [{"id": "step-1", "description": "Create models", "depends_on": []}]}'
    )
    planner = LLMPlanner(executor=executor)

    result = planner.plan("Build a planner")

    assert isinstance(result, PlanningResult)
    assert result.plan.goal == "Build a planner"
    assert result.plan.steps[0].id == "step-1"
    assert result.raw_response.startswith("{")
    assert result.planner_model == "mock-model"
    assert result.planning_time >= 0.0


def test_llm_planner_requires_executor() -> None:
    planner = LLMPlanner(executor=None)

    with pytest.raises(RuntimeError, match="requires an executor"):
        planner.plan("Build a planner")