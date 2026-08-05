from armo.models import SubTask


class PromptBuilder:
    """
    Converts a SubTask into a prompt suitable for an LLM.
    """

    @staticmethod
    def build(task: SubTask) -> str:
        return f"""You are an expert AI agent.

Task ID:
{task.id}

Capability:
{task.capability.value}

Difficulty:
{task.difficulty:.2f}

Task:
{task.description}

Provide a clear, accurate answer.
"""