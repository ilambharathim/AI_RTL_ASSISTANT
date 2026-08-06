"""
Netlist module IR node.
"""

from dataclasses import dataclass, field

from app.ir.netlist_instance import (
    NetlistInstance,
)


@dataclass(slots=True)
class NetlistModule:

    name: str

    instances: list[
        NetlistInstance
    ] = field(
        default_factory=list,
    )

