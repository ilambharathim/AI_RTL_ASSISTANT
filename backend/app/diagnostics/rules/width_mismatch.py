"""
Width Mismatch Detection.

Detects assignments whose source width exceeds the
destination width.
"""

from app.ast import (
    ContinuousAssign,
    ProceduralAssignment,
    ModuleDeclaration,
    CompilationUnit,
    AlwaysBlock,
    StatementBlock,
    IfStatement,
)

from app.ast.expression import (
    IdentifierExpression,
)

from app.diagnostics.base.diagnostic_rule import (
    DiagnosticRule,
)

from app.diagnostics.diagnostic import (
    Diagnostic,
)


class WidthMismatchRule(DiagnosticRule):

    code = "RIVA3001"

    name = "Width Mismatch"

    def run(
        self,
        semantic_model,
    ):

        self.semantic_model = semantic_model

        diagnostics = []

        self.diagnostics = diagnostics

        self._visit(
            semantic_model.syntax_tree,
        )

        return diagnostics

    def _visit(
        self,
        node,
    ):

        if node is None:
            return

        if isinstance(
            node,
            CompilationUnit,
        ):

            for declaration in node.declarations:

                self._visit(
                    declaration,
                )

            return

        if isinstance(
            node,
            ModuleDeclaration,
        ):

            for member in node.members:

                self._visit(
                    member,
                )

            return

        if isinstance(
            node,
            AlwaysBlock,
        ):

            for statement in node.statements:

                self._visit(
                    statement,
                )

            return

        if isinstance(
            node,
            StatementBlock,
        ):

            for statement in node.statements:

                self._visit(
                    statement,
                )

            return

        if isinstance(
            node,
            IfStatement,
        ):

            self._visit(
                node.then_branch,
            )

            self._visit(
                node.else_branch,
            )

            return

        if isinstance(
            node,
            (
                ContinuousAssign,
                ProceduralAssignment,
            ),
        ):

            self._check_assignment(
                node,
            )

    def _check_assignment(
        self,
        assignment,
    ):

        symbols = self.semantic_model.symbols

        target = symbols.get(
            assignment.target,
        )

        if target is None:
            return

        destination_width = target.width

        if destination_width is None:
            return

        expression = assignment.expression

        if not isinstance(
            expression,
            IdentifierExpression,
        ):
            return

        source = symbols.get(
            expression.name,
        )

        if source is None:
            return

        source_width = source.width

        if source_width is None:
            return

        if source_width > destination_width:

            self.diagnostics.append(

                Diagnostic(

                    severity="warning",

                    code=self.code,

                    message=(
                        f"Width mismatch: "
                        f"{assignment.target} "
                        f"({destination_width} bits) <- "
                        f"{expression.name} "
                        f"({source_width} bits)"
                    ),

                    suggestion=(
                        "Slice or resize the source signal."
                    ),

                )

            )
