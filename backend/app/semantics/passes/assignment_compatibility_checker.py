"""
Assignment Compatibility Checker.

Checks width compatibility between procedural assignments.
"""

from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    ProceduralAssignment,
)

from app.ast.expression import (
    IdentifierExpression,
)

from app.diagnostics.diagnostic import Diagnostic
from app.diagnostics.catalog.width_catalog import RIVA3001


class AssignmentCompatibilityChecker:

    def check(
        self,
        tree,
        model,
    ):

        if isinstance(
            tree,
            CompilationUnit,
        ):

            for declaration in tree.declarations:

                self.check(
                    declaration,
                    model,
                )

            return

        if isinstance(
            tree,
            ModuleDeclaration,
        ):

            for member in tree.members:

                self.check(
                    member,
                    model,
                )

            return

        if isinstance(
            tree,
            ProceduralAssignment,
        ):

            self._check_assignment(
                tree,
                model,
            )

    def _check_assignment(
        self,
        assignment,
        model,
    ):

        lhs = assignment.target

        if lhs not in model.types:
            return

        expression = assignment.expression

        if not isinstance(
            expression,
            IdentifierExpression,
        ):
            return

        rhs = expression.name

        if rhs not in model.types:
            return

        lhs_width = model.types[lhs].get(
            "width",
        )

        rhs_width = model.types[rhs].get(
            "width",
        )

        if (
            lhs_width is None
            or rhs_width is None
        ):
            return

        if lhs_width == rhs_width:
            return

        model.diagnostics.append(

            Diagnostic(

                code=RIVA3001.code,

                category=RIVA3001.category,

                severity=RIVA3001.severity,

                message=(
                    f"Width mismatch: "
                    f"{lhs} ({lhs_width} bits) <- "
                    f"{rhs} ({rhs_width} bits)"
                ),

                explanation=RIVA3001.explanation,

                suggestion=RIVA3001.suggestion,

            )

        )
