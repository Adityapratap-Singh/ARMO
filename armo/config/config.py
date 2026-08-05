from pydantic import BaseModel, Field


class ARMOConfig(BaseModel):
    # --- Confidence thresholds ---
    conf_low: float = Field(default=0.50, ge=0.0, le=1.0)
    disagree_high: float = Field(default=0.35, ge=0.0, le=1.0)
    conf_low2: float = Field(default=0.70, ge=0.0, le=1.0)
    conf_high: float = Field(default=0.80, ge=0.0, le=1.0)

    # --- Graph properties ---
    coupling_low: float = Field(default=0.50, ge=0.0, le=1.0)
    coupling_high: float = Field(default=0.60, ge=0.0, le=1.0)

    # --- Execution ---
    tool_fail_threshold: int = 2
    diff_low: float = Field(default=0.30, ge=0.0, le=1.0)
    bottleneck_high: float = Field(default=0.50, ge=0.0, le=1.0)

    # --- Stability ---
    persistence_min_steps: int = 2

    # --- Runtime overhead ---
    switch_overhead_latency: float = 0.50
    switch_overhead_tokens: int = 80

    # --- Verification ---
    retry_confidence_threshold: float = 0.60