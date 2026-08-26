"""
RIVA RTL semantic type.

RTLType extends the generic semantic Type with
hardware-specific properties.
"""

from dataclasses import dataclass

from app.semantics.types.base.type import Type


@dataclass(frozen=True, slots=True)
class RTLType(Type):
    """
    Semantic type for RTL values.

    width:
        Effective number of bits.

    signed:
        Whether the value is signed.

    packed:
        Whether the value is represented as a packed vector.
    """

    width: int = 1

    signed: bool = False

    packed: bool = False
