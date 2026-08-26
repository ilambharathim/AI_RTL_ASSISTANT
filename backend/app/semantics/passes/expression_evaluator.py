"""
Constant expression evaluator.
"""

from app.ast.expression import (
    IdentifierExpression,
    LiteralExpression,
    UnaryExpression,
    BinaryExpression,
)


class ExpressionEvaluator:

    @staticmethod
    def evaluate(expr, constants=None):
        if constants is None:
            constants = {}

        if isinstance(expr, LiteralExpression):
            return int(expr.value)

        if isinstance(expr, IdentifierExpression):
            if expr.name in constants:
                val = constants[expr.name]
                if isinstance(val, int):
                    return val
                try:
                    return int(val)
                except (ValueError, TypeError):
                    pass
            # Default fallback for un-evaluated parameter identifiers in range expressions
            return 1

        if isinstance(expr, UnaryExpression):

            value = ExpressionEvaluator.evaluate(
                expr.operand,
                constants=constants,
            )

            if expr.operator == "-":
                return -value

            if expr.operator == "+":
                return value

        if isinstance(expr, BinaryExpression):

            left = ExpressionEvaluator.evaluate(
                expr.left,
                constants=constants,
            )

            right = ExpressionEvaluator.evaluate(
                expr.right,
                constants=constants,
            )

            if expr.operator == "+":
                return left + right

            if expr.operator == "-":
                return left - right

            if expr.operator == "*":
                return left * right

            if expr.operator == "/":
                return left // right if right != 0 else 0

        raise RuntimeError(
            f"Unsupported constant expression: {expr}"
        )
