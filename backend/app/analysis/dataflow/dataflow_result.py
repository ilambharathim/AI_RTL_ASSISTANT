"""
Data Flow Result.
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class DataFlowResult:

    in_sets: dict = field(
        default_factory=dict,
    )

    out_sets: dict = field(
        default_factory=dict,
    )
