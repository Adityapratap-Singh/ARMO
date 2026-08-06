from armo.topology.factory import TopologyFactory
from armo.topology.types import TopologyType


def test_factory_creates_registered_topology() -> None:
    factory = TopologyFactory()
    topology = factory.create(TopologyType.CHAIN)

    assert topology is not None
    assert topology.name == "chain"
