"""
Bound instance.
"""

from dataclasses import dataclass, field

from app.elaboration.model.port_binding import PortBinding


@dataclass(slots=True)
class BoundInstance:

    instance_name: str

    module_name: str

    bindings: list[PortBinding] = field(
        default_factory=list,
    )

