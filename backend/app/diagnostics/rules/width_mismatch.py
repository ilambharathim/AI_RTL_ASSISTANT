"""
Width Mismatch Detection.

Detects assignments whose source and destination widths differ.
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

from app.diagnostics.catalog.width_catalog import (
    RIVA3001,
)


class WidthMismatchRule(DiagnosticRule):

    code = RIVA3001.code
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

        expression = assignment.expression

        if not isinstance(
            expression,
            IdentifierExpression,
        ):
            return

        target_name = assignment.target
        source_name = expression.name

        types = self.semantic_model.types

        target_info = types.get(
            target_name,
        )

        source_info = types.get(
            source_name,
        )

        if target_info is None:
            return

        if source_info is None:
            return

        destination_width = target_info.get(
            "width",
        )

        source_width = source_info.get(
            "width",
        )

        if destination_width is None:
            return

        if source_width is None:
            return

        if source_width == destination_width:
            return

        self.diagnostics.append(

            Diagnostic(

                code=RIVA3001.code,

                category=RIVA3001.category,

                severity=RIVA3001.severity,

                message=(
                    f"Width mismatch: "
                    f"{target_name} "
                    f"({destination_width} bits) <- "
                    f"{source_name} "
                    f"({source_width} bits)"
                ),

                explanation=RIVA3001.explanation,

                suggestion=RIVA3001.suggestion,

            )

        )
