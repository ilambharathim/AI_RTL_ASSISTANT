"""
Identifier Checker.

Detects identifiers that cannot be resolved in the semantic model.
"""

from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    SignalDeclaration,
    ParameterDeclaration,
    ProceduralAssignment,
)

from app.ast.expression import (
    IdentifierExpression,
    BinaryExpression,
    UnaryExpression,
)

from app.diagnostics.diagnostic import Diagnostic
from app.diagnostics.catalog.semantic_catalog import RIVA1001


class IdentifierChecker:

    def check(self, tree, model):

        if isinstance(tree, CompilationUnit):

            for declaration in tree.declarations:
                self.check(declaration, model)

            return

        if isinstance(tree, ModuleDeclaration):

            for member in tree.members:
                self.check(member, model)

            return

        if isinstance(tree, SignalDeclaration):
            return

        if isinstance(tree, ParameterDeclaration):

            self._check_expression(
                tree.value,
                model,
            )

            return

        if isinstance(tree, ProceduralAssignment):

            self._check_expression(
                tree.expression,
                model,
            )

            return

    def _check_expression(
        self,
        expression,
        model,
    ):

        if isinstance(
            expression,
            IdentifierExpression,
        ):

            if (
                expression.name not in model.types
                and expression.name not in model.constant_values
            ):

                model.diagnostics.append(
                    Diagnostic(
                        code=RIVA1001.code,
                        category=RIVA1001.category,
                        severity=RIVA1001.severity,
                        message=(
                            f"Identifier '{expression.name}' "
                            "is not declared."
                        ),
                        explanation=RIVA1001.explanation,
                        suggestion=RIVA1001.suggestion,
                    )
                )

            return

        if isinstance(
            expression,
            BinaryExpression,
        ):

            self._check_expression(
                expression.left,
                model,
            )

            self._check_expression(
                expression.right,
                model,
            )

            return

        if isinstance(
            expression,
            UnaryExpression,
        ):

            self._check_expression(
                expression.operand,
                model,
            )

            return
