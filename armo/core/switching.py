from armo.config import ARMOConfig
from armo.models import RuntimeSignals, Topology, SwitchReason


class SwitchingDecision:
    def __init__(
        self,
        topology: Topology | None,
        reason: SwitchReason = SwitchReason.NONE,
    ):
        self.topology = topology
        self.reason = reason

    @property
    def should_switch(self) -> bool:
        return self.topology is not None

    def __repr__(self):
        return (
            f"SwitchingDecision("
            f"topology={self.topology}, "
            f"reason={self.reason})"
        )


class SwitchingPolicy:
    """
    Implements the six ARMO switching rules.
    """

    def __init__(self, config: ARMOConfig):
        self.config = config

    def evaluate(self, signals: RuntimeSignals) -> SwitchingDecision:

        # Rule 1
        if signals.average_confidence < self.config.conf_low:
            return SwitchingDecision(
                Topology.EVALUATOR_OPTIMIZER,
                SwitchReason.LOW_CONFIDENCE,
            )

        # Rule 2
        if (
            signals.disagreement > self.config.disagree_high
            and signals.average_confidence < self.config.conf_low2
        ):
            return SwitchingDecision(
                Topology.EVALUATOR_OPTIMIZER,
                SwitchReason.HIGH_DISAGREEMENT,
            )

        # Rule 3
        if (
            signals.average_confidence > self.config.conf_high
            and signals.coupling < self.config.coupling_low
            and signals.parallelizable_ratio > 0.5
        ):
            return SwitchingDecision(
                Topology.PARALLEL,
                SwitchReason.PARALLELISM,
            )

        # Rule 4
        if signals.tool_failures >= self.config.tool_fail_threshold:
            return SwitchingDecision(
                Topology.PLANNER_WORKER,
                SwitchReason.TOOL_FAILURE,
            )

        # Rule 5
        if signals.remaining_difficulty < self.config.diff_low:
            return SwitchingDecision(
                Topology.ROUTING,
                SwitchReason.LOW_DIFFICULTY,
            )

        # Rule 6
        if (
            signals.bottleneck > self.config.bottleneck_high
            and signals.coupling > self.config.coupling_high
        ):
            return SwitchingDecision(
                Topology.SEQUENTIAL,
                SwitchReason.BOTTLENECK,
            )

        return SwitchingDecision(None)