"""
Netlist IR.
"""

from dataclasses import dataclass, field

from app.ir.netlist_module import (
    NetlistModule,
)


@dataclass(slots=True)
class Netlist:

    modules: dict[
        str,
        NetlistModule,
    ] = field(
        default_factory=dict,
    )

