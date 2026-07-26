"""
Hardware port domain model.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.shared.source_location import SourceLocation


@dataclass(slots=True)
class Port:
    """
    Represents a hardware module port.

    The model describes ports from Verilog/SystemVerilog modules, interfaces,
    and IP blocks while preserving the originating specification location.
    """

    name: str
    direction: str
    datatype: str = "logic"
    width: int = 1
    signed: bool = False
    packed_dimensions: list[str] = field(default_factory=list)
    unpacked_dimensions: list[str] = field(default_factory=list)
    default_value: str | None = None
    interface: str | None = None
    description: str = ""
    source_location: SourceLocation = field(default_factory=SourceLocation)

    def __post_init__(self) -> None:
        if not isinstance(self.source_location, SourceLocation):
            raise TypeError(
                "source_location must be a SourceLocation."
            )
