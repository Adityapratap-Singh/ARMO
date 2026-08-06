# Runtime Execution Engine

The runtime execution engine is the first sequential execution layer for ARMO.

## Pipeline

ExecutionGraph -> RuntimeEngine -> Dispatcher -> Worker -> Executor -> RuntimeHistory

## Responsibilities

- RuntimeEngine orchestrates the execution loop.
- Dispatcher picks the next ready node.
- Worker runs a single node through the executor backend.
- Runtime events and history capture lifecycle transitions.

## Execution flow

1. The engine initializes runtime state from the execution graph.
2. It repeatedly looks for ready nodes.
3. A single ready node is dispatched and executed.
4. Completed nodes unlock their dependents.
5. The loop continues until the graph is finished or a node fails.

## Failure behavior

If an executor raises an exception, the engine marks the node as failed, records a runtime event, and stops execution.

## Notes

This first phase is sequential by design. Parallel execution will be introduced in a later phase.
