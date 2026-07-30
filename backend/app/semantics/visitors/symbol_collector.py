"""
Collect declared symbols.
"""

from app.ast import (
    ModuleDeclaration,
    SignalDeclaration,
    ParameterDeclaration,
)

from app.semantics.semantic_diagnostic import SemanticDiagnostic
from app.semantics.symbol import Symbol
from app.semantics.symbol_kind import SymbolKind


class SymbolCollector:

    def __init__(self):

        self.diagnostics = []

    def collect(
        self,
        scope,
        node,
    ):

        if isinstance(node, ModuleDeclaration):

            symbol = Symbol(
                node.name,
                SymbolKind.MODULE,
                node,
            )

        elif isinstance(node, ParameterDeclaration):

            symbol = Symbol(
                node.name,
                SymbolKind.PARAMETER,
                node,
            )

        elif isinstance(node, SignalDeclaration):

            symbol = Symbol(
                node.name,
                SymbolKind.SIGNAL,
                node,
            )

        else:
            return

        #
        # Shadowing warning
        #
        if scope.lookup_parent(symbol.name) is not None:

            self.diagnostics.append(
                SemanticDiagnostic(
                    f"'{symbol.name}' shadows outer declaration."
                )
            )

        try:

            scope.define(symbol)

        except RuntimeError as error:

            self.diagnostics.append(
                SemanticDiagnostic(
                    str(error)
                )
            )
