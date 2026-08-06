"""
RTL semantic type.

Extends the generic semantic Type with
hardware-specific properties.
"""

from dataclasses import dataclass

from app.semantics.types.base.type import Type


@dataclass(frozen=True, slots=True)
class RTLType(Type):
    """
    Base class for every RTL semantic type.
    """

    width: int = 1

    signed: bool = False

    packed: bool = False
