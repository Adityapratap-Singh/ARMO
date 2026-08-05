from __future__ import annotations

import time

import ollama

from armo.executor.prompts import PromptBuilder
from armo.executor.registry import ModelRegistry
from armo.models import AgentResult, ModelTier, SubTask
from .base import BaseExecutor


class OllamaExecutor(BaseExecutor):
    """
    Executes subtasks using a local Ollama model.
    """

    def __init__(self, tier: ModelTier = ModelTier.STRONG):
        self.registry = ModelRegistry()
        self.model = self.registry.get(tier)

    def execute(self, task: SubTask) -> AgentResult:

        prompt = PromptBuilder.build(task)

        start = time.perf_counter()

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        latency = time.perf_counter() - start

        text = response["message"]["content"]

        return AgentResult(
            subtask_id=task.id,
            output=text,
            confidence=1.0,
            latency=latency,
            token_cost=len(text.split()),
            dollar_cost=0.0,
            tool_failures=0,
        )