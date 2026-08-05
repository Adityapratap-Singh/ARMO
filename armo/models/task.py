from pydantic import BaseModel, Field
from .enums import Capability, TaskType


class SubTask(BaseModel):
    id: str
    description: str
    capability: Capability
    difficulty: float = Field(ge=0.0, le=1.0)
    dependencies: list[str] = Field(default_factory=list)


class TaskProfile(BaseModel):
    id: str
    description: str
    task_type: TaskType

    subtasks: list[SubTask]

    parallelism_width: float = Field(ge=0.0, le=1.0)
    coupling_density: float = Field(ge=0.0, le=1.0)

    critical_path_depth: int = Field(ge=1)

    requires_verification: bool = False