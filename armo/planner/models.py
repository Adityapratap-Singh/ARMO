from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PlanningStep:
    id: str
    description: str
    depends_on: list[str] = field(default_factory=list)


@dataclass
class TaskPlan:
    goal: str
    steps: list[PlanningStep] = field(default_factory=list)

    def add_step(self, step: PlanningStep) -> None:
        self.steps.append(step)

    @property
    def step_count(self) -> int:
        return len(self.steps)

    @property
    def is_empty(self) -> bool:
        return self.step_count == 0


@dataclass
class PlanningResult:
    plan: TaskPlan
    raw_response: str
    planner_model: str
    planning_time: float
