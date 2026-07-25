from dataclasses import dataclass, field
from typing import Optional, List


@dataclass(slots=True)
class Port:
    """
    Represents a hardware module port.

    This model is universal enough to describe ports from
    Verilog/SystemVerilog modules, interfaces and IP blocks.
    """

    name: str

    direction: str  # input | output | inout

    datatype: str = "logic"

    width: int = 1

    signed: bool = False

    packed_dimensions: List[str] = field(default_factory=list)

    unpacked_dimensions: List[str] = field(default_factory=list)

    default_value: Optional[str] = None

    interface: Optional[str] = None

    description: str = ""
