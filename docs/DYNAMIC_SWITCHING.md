# Dynamic Topology Switching

## Overview

Phase 5 introduces the first runtime-level topology switching infrastructure for ARMO.
The runtime can now receive a switching decision after each completed node, route it through a topology manager, and record the transition without changing graph semantics yet.

## Architecture

```text
ExecutionNode
    ↓
SignalEngine
    ↓
SwitchingPolicy
    ↓
TopologyManager
    ↓
RuntimeHistory
```

## Lifecycle

1. The runtime executes a node.
2. The result is converted into runtime signals.
3. The switching policy produces a decision.
4. The topology manager receives the decision.
5. A new topology object is created and used to transform the current graph.
6. The state and history are updated with the switch details.

## Event Sequence

- TOPOLOGY_SWITCH_REQUESTED
- TOPOLOGY_SWITCH_STARTED
- TOPOLOGY_SWITCH_COMPLETED

## Current Behavior

The initial implementation uses identity transforms.
That means the runtime behavior remains sequential and graph semantics stay unchanged, but the infrastructure for switching is now in place and extensible.

## Future Roadmap

Future phases can implement real graph transformations such as:

- parallel branch expansion,
- evaluator/optimizer rewiring,
- planner/executor handoff,
- reflection and consensus topology rewrites.
