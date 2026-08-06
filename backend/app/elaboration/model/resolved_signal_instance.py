"""
Resolved signal instance.
"""

from dataclasses import dataclass, field

from app.elaboration.model.resolved_signal import (
    ResolvedSignal,
)


@dataclass(slots=True)
class ResolvedSignalInstance:

    instance_name: str

    module_name: str

    ports: list[
        ResolvedSignal
    ] = field(
        default_factory=list,
    )

