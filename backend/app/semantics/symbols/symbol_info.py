"""
Semantic symbol information.

SymbolInfo is the semantic information attached to
a resolved declaration.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class SymbolInfo:
    """
    Resolved semantic information for a symbol.
    """

    name: str

    symbol_type: str

    width: int | None = None

    signed: bool = False

    constant_value: object = None

    declaration: object | None = None

    semantic_type: object | None = None
