"""
Parameter Type Checker.

Validates identifiers referenced by parameter declarations.
"""

from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    ParameterDeclaration,
)

from app.ast.expression import IdentifierExpression


class ParameterTypeChecker:

    def check(
        self,
        tree,
        model,
    ):

        if isinstance(tree, CompilationUnit):

            for declaration in tree.declarations:
                self.check(
                    declaration,
                    model,
                )

            return

        if isinstance(tree, ModuleDeclaration):

            for member in tree.members:
                self.check(
                    member,
                    model,
                )

            return

        if isinstance(tree, ParameterDeclaration):

            value = tree.value

            if isinstance(
                value,
                IdentifierExpression,
            ):

                if (
                    value.name not in model.types
                    and value.name not in model.constant_values
                ):

                    model.diagnostics.append(
                        {
                            "kind": "UnknownParameterType",
                            "parameter": tree.name,
                            "identifier": value.name,
                        }
                    )
