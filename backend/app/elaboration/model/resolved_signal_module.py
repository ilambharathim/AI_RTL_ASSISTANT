"""
Resolved signal module.
"""

from dataclasses import dataclass, field

from app.elaboration.model.resolved_signal_instance import (
    ResolvedSignalInstance,
)


@dataclass(slots=True)
class ResolvedSignalModule:

    name: str

    instances: list[
        ResolvedSignalInstance
    ] = field(
        default_factory=list,
    )

