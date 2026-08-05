from pydantic import BaseModel, Field


class RuntimeSignals(BaseModel):
    """
    Live execution signals collected after every orchestration step.
    These are the inputs to ARMO's switching policy.
    """

    average_confidence: float = Field(ge=0.0, le=1.0)

    disagreement: float = Field(ge=0.0, le=1.0)

    tool_failures: int = 0

    bottleneck: float = Field(ge=0.0)

    remaining_difficulty: float = Field(ge=0.0, le=1.0)

    parallelizable_ratio: float = Field(default=0.0, ge=0.0, le=1.0)

    coupling: float = Field(default=0.0, ge=0.0, le=1.0)