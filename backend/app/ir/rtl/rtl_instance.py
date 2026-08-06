"""
RTL Instance.
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class RTLInstance:

    name: str

    module: str

    ports: dict = field(
        default_factory=dict,
    )

