"""
Implicit Net Detector.

Detects identifiers that are referenced but not declared.
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
    FunctionCallExpression,
)


class ImplicitNetDetector:

    def detect(self, tree, model):

        diagnostics = []

        if isinstance(tree, CompilationUnit):

            for declaration in tree.declarations:
                diagnostics.extend(
                    self.detect(
                        declaration,
                        model,
                    )
                )

            return diagnostics

        if isinstance(tree, ModuleDeclaration):

            declared = set()

            for port in tree.ports:
                if hasattr(port, "name"):
                    declared.add(port.name)

            for member in tree.members:

                if isinstance(
                    member,
                    (
                        SignalDeclaration,
                        ParameterDeclaration,
                    ),
                ):
                    declared.add(member.name)

            for member in tree.members:

                if isinstance(
                    member,
                    ProceduralAssignment,
                ):
                    diagnostics.extend(
                        self._check_expression(
                            member.expression,
                            declared,
                            model,
                        )
                    )

            return diagnostics

        return diagnostics

    def _check_expression(
        self,
        expression,
        declared,
        model,
    ):

        diagnostics = []

        if isinstance(
            expression,
            IdentifierExpression,
        ):

            if expression.name not in declared:

                diagnostics.append(
                    f"Implicit net '{expression.name}'."
                )

            return diagnostics

        if isinstance(
            expression,
            BinaryExpression,
        ):

            diagnostics.extend(
                self._check_expression(
                    expression.left,
                    declared,
                    model,
                )
            )

            diagnostics.extend(
                self._check_expression(
                    expression.right,
                    declared,
                    model,
                )
            )

            return diagnostics

        if isinstance(
            expression,
            UnaryExpression,
        ):

            diagnostics.extend(
                self._check_expression(
                    expression.operand,
                    declared,
                    model,
                )
            )

            return diagnostics

        if isinstance(
            expression,
            FunctionCallExpression,
        ):

            for argument in expression.arguments:

                diagnostics.extend(
                    self._check_expression(
                        argument,
                        declared,
                        model,
                    )
                )

            return diagnostics

        return diagnostics
