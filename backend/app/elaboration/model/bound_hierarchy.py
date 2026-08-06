"""
Bound hierarchy.
"""

from dataclasses import dataclass, field

from app.elaboration.model.bound_module import BoundModule


@dataclass(slots=True)
class BoundHierarchy:

    modules: dict[str, BoundModule] = field(
        default_factory=dict,
    )

