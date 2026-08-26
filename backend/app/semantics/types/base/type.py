"""
RIVA Base Semantic Type.

The parser produces syntax.
The semantic analyzer produces semantic Type objects.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Type:
    """
    Base class for every semantic type.

    A Type represents semantic meaning rather than
    source-level syntax.
    """

    name: str

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(name={self.name!r})"
        )
