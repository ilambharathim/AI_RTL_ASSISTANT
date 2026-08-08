"""
Expression Type Checker.

Infers type information for expressions.
"""

from app.ast.expression import (
    IdentifierExpression,
    LiteralExpression,
    BinaryExpression,
)


class ExpressionTypeChecker:

    def infer(
        self,
        expression,
        model,
    ):

        #
        # Identifier
        #
        if isinstance(expression, IdentifierExpression):

            return model.types.get(
                expression.name,
                None,
            )

        #
        # Integer literal
        #
        if isinstance(expression, LiteralExpression):

            return {
                "type": "int",
                "width": 32,
                "signed": True,
            }

        #
        # Binary expression
        #
        if isinstance(expression, BinaryExpression):

            left = self.infer(
                expression.left,
                model,
            )

            right = self.infer(
                expression.right,
                model,
            )

            if left is None or right is None:
                return None

            return {
                "type": left["type"],
                "width": max(
                    left["width"],
                    right["width"],
                ),
                "signed": (
                    left["signed"]
                    or right["signed"]
                ),
            }

        return None
