"""
RTL Graph.
"""

from dataclasses import dataclass, field

from app.ir.rtl.rtl_module import RTLModule


@dataclass(slots=True)
class RTLGraph:

    modules: dict[str, RTLModule] = field(
        default_factory=dict,
    )

