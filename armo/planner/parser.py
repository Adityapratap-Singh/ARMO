from __future__ import annotations

import json
from typing import Any

from .models import PlanningStep, TaskPlan


class PlanningParser:
    """Parse and validate LLM planner JSON into ARMO task plans."""

    @staticmethod
    def parse(raw_json: str) -> TaskPlan:
        try:
            payload = json.loads(raw_json)
        except json.JSONDecodeError as exc:
            raise ValueError("Planner response was not valid JSON") from exc

        if not isinstance(payload, dict):
            raise ValueError("Planner response must be a JSON object")

        goal = payload.get("goal")
        if not isinstance(goal, str) or not goal.strip():
            raise ValueError("Planner response must include a non-empty goal")

        steps_payload = payload.get("steps")
        if not isinstance(steps_payload, list):
            raise ValueError("Planner response must include a steps array")

        plan = TaskPlan(goal=goal.strip())

        for step_payload in steps_payload:
            if not isinstance(step_payload, dict):
                raise ValueError("Each planner step must be a JSON object")

            step_id = step_payload.get("id")
            description = step_payload.get("description")
            depends_on = step_payload.get("depends_on", [])

            if not isinstance(step_id, str) or not step_id.strip():
                raise ValueError("Each planner step must include a non-empty id")
            if not isinstance(description, str) or not description.strip():
                raise ValueError("Each planner step must include a non-empty description")
            if not isinstance(depends_on, list) or not all(
                isinstance(dep, str) for dep in depends_on
            ):
                raise ValueError("Planner step depends_on must be a list of strings")

            plan.add_step(
                PlanningStep(
                    id=step_id.strip(),
                    description=description.strip(),
                    depends_on=list(depends_on),
                )
            )

        return plan