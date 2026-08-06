"""
Resolved signal hierarchy.
"""

from dataclasses import dataclass, field

from app.elaboration.model.resolved_signal_module import (
    ResolvedSignalModule,
)


@dataclass(slots=True)
class ResolvedSignalHierarchy:

    modules: dict[
        str,
        ResolvedSignalModule,
    ] = field(
        default_factory=dict,
    )

