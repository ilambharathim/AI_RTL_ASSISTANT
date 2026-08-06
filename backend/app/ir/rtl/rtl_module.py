"""
RTL Module.
"""

from dataclasses import dataclass, field

from app.ir.rtl.rtl_instance import RTLInstance


@dataclass(slots=True)
class RTLModule:

    name: str

    instances: list[RTLInstance] = field(
        default_factory=list,
    )

