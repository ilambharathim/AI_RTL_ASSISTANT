"""
Compiler symbol representation.
"""

from dataclasses import dataclass

from app.semantics.symbol_kind import SymbolKind


@dataclass(slots=True)
class Symbol:
    """
    Represents one declared object in a scope.
    """

    name: str

    kind: SymbolKind

    declaration: object | None = None
