"""
Semantic scope object.
"""

from dataclasses import dataclass, field

from app.semantics.scope_kind import ScopeKind
from app.semantics.symbol import Symbol


@dataclass(slots=True)
class Scope:

    name: str

    kind: ScopeKind

    parent: "Scope | None" = None

    children: list["Scope"] = field(default_factory=list)

    symbols: dict[str, Symbol] = field(default_factory=dict)

    def add_child(
        self,
        child: "Scope",
    ):

        self.children.append(child)

    def lookup_local(
        self,
        name: str,
    ):

        return self.symbols.get(name)

    def lookup(
        self,
        name: str,
    ):

        scope = self

        while scope is not None:

            symbol = scope.lookup_local(name)

            if symbol is not None:
                return symbol

            scope = scope.parent

        return None

    def lookup_parent(
        self,
        name: str,
    ):

        scope = self.parent

        while scope is not None:

            symbol = scope.lookup_local(name)

            if symbol is not None:
                return symbol

            scope = scope.parent

        return None

    def define(
        self,
        symbol: Symbol,
    ):

        if symbol.name in self.symbols:

            raise RuntimeError(
                f"Duplicate symbol '{symbol.name}' in scope '{self.name}'."
            )

        self.symbols[symbol.name] = symbol
