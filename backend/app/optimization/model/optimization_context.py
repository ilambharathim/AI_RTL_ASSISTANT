"""
Optimization context.

Shared state for optimization passes.
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class OptimizationContext:

    changed: bool = False

    statistics: dict = field(
        default_factory=dict,
    )

    iteration: int = 0

