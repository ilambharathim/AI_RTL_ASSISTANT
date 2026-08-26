"""
Semantic scope object.
"""

from dataclasses import dataclass, field

from app.semantics.scope_kind import ScopeKind
from app.semantics.symbol import Symbol


@dataclass(slots=True)
class Scope:
    """
    Lexical scope containing symbol declarations.
    """

    name: str

    kind: ScopeKind

    parent: "Scope | None" = None

    children: list["Scope"] = field(
        default_factory=list,
    )

    symbols: dict[str, Symbol] = field(
        default_factory=dict,
    )

    def add_child(
        self,
        child: "Scope",
    ):
        """
        Attach a child scope.
        """

        if child not in self.children:
            self.children.append(child)

    def lookup_local(
        self,
        name: str,
    ):
        """
        Look up a symbol only in this scope.
        """

        return self.symbols.get(name)

    def lookup(
        self,
        name: str,
    ):
        """
        Resolve a symbol from this scope outward
        through its parent scopes.
        """

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
        """
        Resolve a symbol only in parent scopes.
        """

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
        """
        Define a symbol in this scope.

        Duplicate declarations are rejected.
        """

        if symbol.name in self.symbols:
            raise RuntimeError(
                f"Duplicate symbol "
                f"'{symbol.name}' "
                f"in scope '{self.name}'."
            )

        self.symbols[symbol.name] = symbol
