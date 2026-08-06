from armo.topology.base import BaseTopology
from armo.topology.registry import TopologyRegistry
from armo.topology.types import TopologyType


class DummyTopology(BaseTopology):
    name = "dummy"

    def transform(self, graph, runtime_state):
        return graph


def test_registry_registers_and_returns_topology() -> None:
    registry = TopologyRegistry()
    registry.register(TopologyType.CHAIN, DummyTopology)

    topology_cls = registry.get(TopologyType.CHAIN)

    assert topology_cls is DummyTopology
    assert TopologyType.CHAIN in registry.available()
