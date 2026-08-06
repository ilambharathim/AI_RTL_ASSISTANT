"""
Bound module.
"""

from dataclasses import dataclass, field

from app.elaboration.model.bound_instance import BoundInstance


@dataclass(slots=True)
class BoundModule:

    name: str

    instances: list[BoundInstance] = field(
        default_factory=list,
    )

