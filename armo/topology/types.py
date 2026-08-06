from enum import Enum


class TopologyType(str, Enum):
    CHAIN = "chain"
    PARALLEL = "parallel"
    EVALUATOR_OPTIMIZER = "evaluator_optimizer"
    PLANNER_EXECUTOR = "planner_executor"
    REFLECTION = "reflection"
    CONSENSUS = "consensus"
