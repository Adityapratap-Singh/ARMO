from __future__ import annotations

from typing import Type

from armo.topology.base import BaseTopology
from armo.topology.types import TopologyType


class TopologyRegistry:
    """Registry of available topology implementations."""

    def __init__(self) -> None:
        self._registry: dict[TopologyType, Type[BaseTopology]] = {}

    def register(self, topology_type: TopologyType, topology_cls: Type[BaseTopology]) -> None:
        self._registry[topology_type] = topology_cls

    def get(self, topology_type: TopologyType) -> Type[BaseTopology] | None:
        return self._registry.get(topology_type)

    def available(self) -> list[TopologyType]:
        return sorted(self._registry.keys(), key=lambda item: item.value)
