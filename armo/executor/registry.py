from __future__ import annotations

from pathlib import Path

import yaml

from armo.models import ModelTier


class ModelRegistry:
    """
    Loads available models from YAML configuration.
    """

    def __init__(self, config_path: str | None = None):

        if config_path is None:
            config_path = (
                Path(__file__).parent.parent
                / "config"
                / "models.yaml"
            )

        with open(config_path, "r", encoding="utf-8") as f:
            self.models = yaml.safe_load(f)

    def get(self, tier: ModelTier) -> str:
        return self.models[tier.value]