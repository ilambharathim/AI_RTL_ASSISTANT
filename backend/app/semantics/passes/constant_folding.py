"""
Constant Folding Pass.

Evaluates constant expressions at compile time.
"""

from app.ast.expression import (
    LiteralExpression,
    UnaryExpression,
    BinaryExpression,
)

from app.semantics.passes.expression_evaluator import (
    ExpressionEvaluator,
)


class ConstantFolding:

    def fold(
        self,
        node,
    ):

        #
        # Literal
        #
        if isinstance(
            node,
            LiteralExpression,
        ):
            return node

        #
        # Unary
        #
        if isinstance(
            node,
            UnaryExpression,
        ):

            operand = self.fold(
                node.operand,
            )

            if isinstance(
                operand,
                LiteralExpression,
            ):

                value = ExpressionEvaluator.evaluate(
                    UnaryExpression(
                        node.operator,
                        operand,
                    )
                )

                return LiteralExpression(
                    str(value),
                )

            return UnaryExpression(
                node.operator,
                operand,
            )

        #
        # Binary
        #
        if isinstance(
            node,
            BinaryExpression,
        ):

            left = self.fold(
                node.left,
            )

            right = self.fold(
                node.right,
            )

            if (
                isinstance(left, LiteralExpression)
                and isinstance(right, LiteralExpression)
            ):

                value = ExpressionEvaluator.evaluate(
                    BinaryExpression(
                        node.operator,
                        left,
                        right,
                    )
                )

                return LiteralExpression(
                    str(value),
                )

            return BinaryExpression(
                node.operator,
                left,
                right,
            )

        return node
