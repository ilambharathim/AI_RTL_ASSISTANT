"""
Netlist instance IR node.
"""

from dataclasses import dataclass, field

from app.ir.net import Net


@dataclass(slots=True)
class NetlistInstance:

    name: str

    module: str

    nets: list[Net] = field(
        default_factory=list,
    )

