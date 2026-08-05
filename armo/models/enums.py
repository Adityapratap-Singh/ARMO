from enum import Enum


class TaskType(str, Enum):
    RESEARCH = "research"
    CODING = "coding"
    REASONING = "reasoning"
    MULTIHOP_QA = "multihop_qa"
    MIXED = "mixed"


class Capability(str, Enum):
    RESEARCH = "research"
    CODING = "coding"
    REASONING = "reasoning"
    VERIFICATION = "verification"
    GENERAL = "general"


class Topology(str, Enum):
    PLANNER_WORKER = "planner_worker"
    PARALLEL = "parallel"
    SEQUENTIAL = "sequential"
    ROUTING = "routing"
    EVALUATOR_OPTIMIZER = "evaluator_optimizer"


class ModelTier(str, Enum):
    STRONG = "strong"
    REASONING = "reasoning"
    CHEAP = "cheap"


class SwitchReason(str, Enum):
    LOW_CONFIDENCE = "low_confidence"
    HIGH_DISAGREEMENT = "high_disagreement"
    PARALLELISM = "parallelism"
    TOOL_FAILURE = "tool_failure"
    LOW_DIFFICULTY = "low_difficulty"
    BOTTLENECK = "bottleneck"
    NONE = "none"