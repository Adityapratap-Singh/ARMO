# Runtime State

## Purpose

The Runtime State is the single source of truth for the ARMO execution engine.

Every component reads from it.

Only the Runtime Engine writes to it.

---

## Contains

### Task

- Current task
- Remaining subtasks
- Completed subtasks

### Execution

- Current topology
- Previous topology
- Active workers
- Execution step

### Metrics

- Total latency
- Total tokens
- Estimated compute cost
- Tool failures

### Signals

- Average confidence
- Disagreement
- Bottleneck
- Parallelism
- Coupling

### Switching

- Last switch reason
- Number of switches
- Persistence counter

### History

- Previous topologies
- Previous signals
- Previous decisions