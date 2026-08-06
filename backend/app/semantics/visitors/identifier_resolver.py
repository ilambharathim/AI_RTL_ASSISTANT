"""
Identifier resolution pass.

Resolves identifiers throughout the AST.
"""

from app.ast import (
    ProceduralAssignment,
    IfStatement,
    StatementBlock,
    AlwaysBlock,
    ModuleDeclaration,
    CompilationUnit,
)

from app.ast.expression import (
    IdentifierExpression,
    LiteralExpression,
    UnaryExpression,
    BinaryExpression,
)


class IdentifierResolver:

    def __init__(self):

        self.errors = []

    def resolve(
        self,
        scope,
        syntax_tree,
    ):

        self.visit(
            scope,
            syntax_tree,
        )

    def visit(
        self,
        scope,
        node,
    ):

        #
        # Compilation unit
        #
        if isinstance(
            node,
            CompilationUnit,
        ):

            for declaration in node.declarations:

                self.visit(
                    scope,
                    declaration,
                )

            return

        #
        # Module
        #
        if isinstance(
            node,
            ModuleDeclaration,
        ):

            for member in node.members:

                self.visit(
                    scope,
                    member,
                )

            return

        #
        # Always block
        #
        if isinstance(
            node,
            AlwaysBlock,
        ):

            for statement in node.statements:

                self.visit(
                    scope,
                    statement,
                )

            return

        #
        # Statement block
        #
        if isinstance(
            node,
            StatementBlock,
        ):

            for statement in node.statements:

                self.visit(
                    scope,
                    statement,
                )

            return

        #
        # If statement
        #
        if isinstance(
            node,
            IfStatement,
        ):

            self._expression(
                scope,
                node.condition,
            )

            self.visit(
                scope,
                node.then_branch,
            )

            if node.else_branch is not None:

                self.visit(
                    scope,
                    node.else_branch,
                )

            return

        #
        # tuple of statements
        #
        if isinstance(
            node,
            tuple,
        ):

            for statement in node:

                self.visit(
                    scope,
                    statement,
                )

            return

        #
        # Assignment
        #
        if isinstance(
            node,
            ProceduralAssignment,
        ):

            if scope.lookup(node.target) is None:

                self.errors.append(
                    f"Undefined identifier '{node.target}'"
                )

            self._expression(
                scope,
                node.expression,
            )

    #
    # Recursive expression resolver
    #
    def _expression(
        self,
        scope,
        expression,
    ):

        if isinstance(
            expression,
            LiteralExpression,
        ):
            return

        if isinstance(
            expression,
            IdentifierExpression,
        ):

            if scope.lookup(expression.name) is None:

                self.errors.append(
                    f"Undefined identifier '{expression.name}'"
                )

            return

        if isinstance(
            expression,
            UnaryExpression,
        ):

            self._expression(
                scope,
                expression.operand,
            )

            return

        if isinstance(
            expression,
            BinaryExpression,
        ):

            self._expression(
                scope,
                expression.left,
            )

            self._expression(
                scope,
                expression.right,
            )

