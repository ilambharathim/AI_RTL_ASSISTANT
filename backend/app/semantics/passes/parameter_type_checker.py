"""
Parameter Type Checker.

Validates identifiers referenced by parameter declarations.

Canonical semantic type information is preferred, while the
legacy model.types representation remains supported.
"""

from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    ParameterDeclaration,
)

from app.ast.expression import (
    IdentifierExpression,
    BinaryExpression,
    UnaryExpression,
)

from app.diagnostics.diagnostic import Diagnostic
from app.diagnostics.catalog.semantic_catalog import RIVA1001


class ParameterTypeChecker:

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
            ParameterDeclaration,
        ):

            self._check_expression(
                tree.value,
                model,
            )

    def _is_declared(
        self,
        name,
        model,
    ):
        """
        Determine whether an identifier is semantically declared.

        Resolution order:

            semantic_types
                ↓
            legacy types
                ↓
            constant_values

        ``symbols`` is intentionally not used here because this
        checker validates parameter-expression references, while
        the existing semantic model uses semantic type and constant
        repositories for this contract.
        """

        semantic_types = getattr(
            model,
            "semantic_types",
            {},
        )

        if name in semantic_types:
            return True

        types = getattr(
            model,
            "types",
            {},
        )

        if name in types:
            return True

        constant_values = getattr(
            model,
            "constant_values",
            {},
        )

        if name in constant_values:
            return True

        return False

    def _check_expression(
        self,
        expression,
        model,
    ):

        if isinstance(
            expression,
            IdentifierExpression,
        ):

            if not self._is_declared(
                expression.name,
                model,
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
                        location=getattr(expression, "location", None),
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
