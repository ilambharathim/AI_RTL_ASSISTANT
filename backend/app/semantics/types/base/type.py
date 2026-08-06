"""
RIVA Base Semantic Type.

Every semantic type in RIVA derives from this class.

The parser produces syntax.

The semantic analyzer produces Type objects.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Type:
    """
    Base class for every semantic type.

    This class represents the semantic meaning of a value,
    not its syntax.
    """

    name: str

    def __str__(self) -> str:

        return self.name

    def __repr__(self) -> str:

        return f"{self.__class__.__name__}(name={self.name!r})"
