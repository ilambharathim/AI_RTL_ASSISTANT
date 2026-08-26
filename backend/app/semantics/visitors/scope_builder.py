"""
Semantic scope builder.
"""

from app.ast import (
    ModuleDeclaration,
    AlwaysBlock,
    IfStatement,
    StatementBlock,
    SignalDeclaration,
    ParameterDeclaration,
)

from app.semantics.scope_kind import ScopeKind
from app.semantics.scope_stack import ScopeStack

from app.semantics.visitors.symbol_collector import SymbolCollector


class ScopeBuilder:
    """
    First semantic pass.

    Builds the complete scope hierarchy while collecting
    declarations into their owning scopes.
    """

    def __init__(self):

        self.scopes = ScopeStack()

        self.collector = SymbolCollector()


    def build(
        self,
        syntax_tree,
    ):
        """
        Backward-compatible API.
        """
        return self.analyze(
            syntax_tree,
        )

    def analyze(
        self,
        syntax_tree,
    ):
        """
        Execute semantic scope construction.
        """
        self.scopes = ScopeStack()
        self.collector = SymbolCollector()

        for declaration in syntax_tree.declarations:

            self.visit(
                declaration,
            )

        return self.scopes.global_scope


    #
    # Internal recursive traversal
    #
    def visit(
        self,
        node,
    ):

        #
        # declarations
        #
        if isinstance(
            node,
            (
                SignalDeclaration,
                ParameterDeclaration,
            ),
        ):

            self.collector.collect(
                self.scopes.current,
                node,
            )

            return

        #
        # module
        #
        if isinstance(
            node,
            ModuleDeclaration,
        ):

            self.collector.collect(
                self.scopes.current,
                node,
            )

            self.scopes.push(
                node.name,
                ScopeKind.MODULE,
            )

            for member in node.members:

                self.visit(
                    member,
                )

            self.scopes.pop()

            return

        #
        # always block
        #
        if isinstance(
            node,
            AlwaysBlock,
        ):

            self.scopes.push(
                "always",
                ScopeKind.PROCEDURAL,
            )

            for statement in node.statements:

                self.visit(
                    statement,
                )

            self.scopes.pop()

            return

        #
        # begin/end block
        #
        if isinstance(
            node,
            StatementBlock,
        ):

            self.scopes.push(
                "begin",
                ScopeKind.PROCEDURAL,
            )

            for statement in node.statements:

                self.visit(
                    statement,
                )

            self.scopes.pop()

            return

        #
        # if statement
        #
        if isinstance(
            node,
            IfStatement,
        ):

            self.scopes.push(
                "if",
                ScopeKind.CONDITIONAL,
            )

            self.visit(
                node.then_branch,
            )

            if node.else_branch is not None:

                self.visit(
                    node.else_branch,
                )

            self.scopes.pop()

            return
