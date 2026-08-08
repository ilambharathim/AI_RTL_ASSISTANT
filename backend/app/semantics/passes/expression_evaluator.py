"""
Constant expression evaluator.
"""

from app.ast.expression import (
    LiteralExpression,
    UnaryExpression,
    BinaryExpression,
)


class ExpressionEvaluator:

    @staticmethod
    def evaluate(expr):

        if isinstance(expr, LiteralExpression):
            return int(expr.value)

        if isinstance(expr, UnaryExpression):

            value = ExpressionEvaluator.evaluate(
                expr.operand,
            )

            if expr.operator == "-":
                return -value

            if expr.operator == "+":
                return value

        if isinstance(expr, BinaryExpression):

            left = ExpressionEvaluator.evaluate(
                expr.left,
            )

            right = ExpressionEvaluator.evaluate(
                expr.right,
            )

            if expr.operator == "+":
                return left + right

            if expr.operator == "-":
                return left - right

            if expr.operator == "*":
                return left * right

            if expr.operator == "/":
                return left // right

        raise RuntimeError(
            f"Unsupported constant expression: {expr}"
        )
