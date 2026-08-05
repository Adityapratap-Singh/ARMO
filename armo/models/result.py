from pydantic import BaseModel


class AgentResult(BaseModel):
    subtask_id: str

    output: str

    confidence: float

    latency: float

    token_cost: int

    dollar_cost: float

    tool_failures: int = 0

    correct: bool | None = None