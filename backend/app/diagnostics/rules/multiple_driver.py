"""
Multiple Driver Detection.

Detects signals driven by more than one source.
"""

from collections import defaultdict

from app.ast import (
    ContinuousAssign,
    ProceduralAssignment,
    AlwaysBlock,
    StatementBlock,
    ModuleDeclaration,
    CompilationUnit,
    IfStatement,
)

from app.diagnostics.base.diagnostic_rule import (
    DiagnosticRule,
)

from app.diagnostics.diagnostic import (
    Diagnostic,
)


class MultipleDriverRule(DiagnosticRule):

    code = "RIVA2001"

    name = "Multiple Driver"

    def run(
        self,
        semantic_model,
    ):

        diagnostics = []

        drivers = defaultdict(int)

        self._visit(
            semantic_model.syntax_tree,
            drivers,
        )

        for signal, count in drivers.items():

            if count > 1:

                diagnostics.append(

                    Diagnostic(

                        severity="error",

                        code=self.code,

                        message=(
                            f"Signal '{signal}' has multiple drivers."
                        ),

                        suggestion=(
                            "Drive a signal from exactly one source."
                        ),

                    )

                )

        return diagnostics

    def _visit(
        self,
        node,
        drivers,
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
                    drivers,
                )

            return

        if isinstance(
            node,
            ModuleDeclaration,
        ):

            for member in node.members:

                self._visit(
                    member,
                    drivers,
                )

            return

        if isinstance(
            node,
            ContinuousAssign,
        ):

            drivers[
                node.target
            ] += 1

            return

        if isinstance(
            node,
            ProceduralAssignment,
        ):

            drivers[
                node.target
            ] += 1

            return

        if isinstance(
            node,
            AlwaysBlock,
        ):

            for statement in node.statements:

                self._visit(
                    statement,
                    drivers,
                )

            return

        if isinstance(
            node,
            StatementBlock,
        ):

            for statement in node.statements:

                self._visit(
                    statement,
                    drivers,
                )

            return

        if isinstance(
            node,
            IfStatement,
        ):

            self._visit(
                node.then_branch,
                drivers,
            )

            self._visit(
                node.else_branch,
                drivers,
            )
