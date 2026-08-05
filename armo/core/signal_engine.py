from statistics import mean, pstdev

from armo.models import AgentResult, RuntimeSignals, SubTask


class SignalEngine:
    """
    Computes runtime signals from execution history.
    """

    @staticmethod
    def compute(
        completed_results: list[AgentResult],
        remaining_subtasks: list[SubTask],
        coupling: float,
    ) -> RuntimeSignals:

        if completed_results:
            confidences = [r.confidence for r in completed_results]
            latencies = [r.latency for r in completed_results]

            avg_conf = mean(confidences)

            disagreement = (
                pstdev(confidences)
                if len(confidences) > 1
                else 0.0
            )

            tool_failures = sum(
                r.tool_failures
                for r in completed_results
            )

            avg_latency = mean(latencies)

            bottleneck = (
                max(latencies) / avg_latency - 1
                if avg_latency > 0
                else 0.0
            )

        else:
            avg_conf = 1.0
            disagreement = 0.0
            tool_failures = 0
            bottleneck = 0.0

        if remaining_subtasks:

            remaining_difficulty = mean(
                s.difficulty
                for s in remaining_subtasks
            )

            parallelizable = sum(
                1
                for s in remaining_subtasks
                if not s.dependencies
            )

            parallel_ratio = (
                parallelizable /
                len(remaining_subtasks)
            )

        else:

            remaining_difficulty = 0.0
            parallel_ratio = 0.0

        return RuntimeSignals(
            average_confidence=avg_conf,
            disagreement=disagreement,
            tool_failures=tool_failures,
            bottleneck=bottleneck,
            remaining_difficulty=remaining_difficulty,
            parallelizable_ratio=parallel_ratio,
            coupling=coupling,
        )