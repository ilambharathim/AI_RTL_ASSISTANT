"""
Semantic symbol information.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class SymbolInfo:

    name: str

    symbol_type: str

    width: int | None = None

    signed: bool = False

    constant_value: object = None

    declaration: object | None = None

