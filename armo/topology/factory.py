from __future__ import annotations

from armo.topology.base import BaseTopology
from armo.topology.registry import TopologyRegistry
from armo.topology.types import TopologyType


class TopologyFactory:
    """Instantiate registered topology implementations."""

    def __init__(self, registry: TopologyRegistry | None = None) -> None:
        self.registry = registry or TopologyRegistry()
        self._register_defaults()

    def _register_defaults(self) -> None:
        from armo.topology.impl import ChainTopology, ParallelTopology

        self.registry.register(TopologyType.CHAIN, ChainTopology)
        self.registry.register(TopologyType.PARALLEL, ParallelTopology)

    def create(self, topology_type: TopologyType) -> BaseTopology | None:
        topology_cls = self.registry.get(topology_type)
        if topology_cls is None:
            return None
        return topology_cls()
