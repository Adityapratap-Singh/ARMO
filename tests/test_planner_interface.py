import pytest

from armo.planner import LLMPlanner


def test_planner_constructor():
    planner = LLMPlanner(executor=None)

    assert planner.executor is None


def test_plan_not_implemented():
    planner = LLMPlanner(executor=None)

    with pytest.raises(NotImplementedError):
        planner.plan("Explain recursion")