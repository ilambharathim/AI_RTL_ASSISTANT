"""
Resolved hierarchy.
"""

from dataclasses import dataclass, field

from app.elaboration.model.resolved_module import (
    ResolvedModule,
)


@dataclass(slots=True)
class ResolvedHierarchy:

    modules: dict[
        str,
        ResolvedModule,
    ] = field(
        default_factory=dict,
    )

