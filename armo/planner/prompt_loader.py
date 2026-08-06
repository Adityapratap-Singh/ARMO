from __future__ import annotations

from pathlib import Path


class PromptLoader:
    """
    Loads planner prompt templates.
    """

    PROMPT_DIR = Path(__file__).parent / "prompts"

    @classmethod
    def load_system_prompt(cls) -> str:
        return (cls.PROMPT_DIR / "planner_system.txt").read_text(
            encoding="utf-8"
        )

    @classmethod
    def load_user_prompt(cls, goal: str) -> str:
        template = (
            cls.PROMPT_DIR / "planner_user.txt"
        ).read_text(encoding="utf-8")

        return template.replace("{{goal}}", goal)