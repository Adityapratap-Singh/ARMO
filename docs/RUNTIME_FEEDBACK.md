# Runtime Feedback Loop

ARMO's runtime feedback loop turns each completed node into execution signals and evaluates whether the current topology should be reconsidered.

## Flow

ExecutionGraph -> RuntimeEngine -> Worker -> Executor -> ExecutionResult -> SignalEngine -> SwitchingPolicy -> RuntimeHistory

## Behavior

- After every completed node, the runtime converts the execution result into runtime signals.
- Signals are passed into the switching policy for evaluation.
- The resulting switching decision is recorded in runtime history.
- Topology switching is not implemented in this phase; the decision is logged only.

## Event emission

The runtime emits events for:

- signal generation
- switching decision evaluation

These events are appended to the runtime history so the execution trace remains observable.
