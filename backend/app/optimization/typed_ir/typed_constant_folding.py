"""
Typed IR Constant Folding.

Evaluates constant expressions in the Typed IR.
"""

from app.ir.ir_expression import (
    IRLiteral,
    IRBinary,
    IRUnary,
)

from app.optimization.model.pass_result import PassResult


class TypedConstantFolding:

    name = "typed_constant_folding"

    def run(
        self,
        semantic_model,
        context,
    ):

        changed = False

        for module in semantic_model.elaboration.ir.values():

            for statement in module.statements:

                if hasattr(statement, "expression"):

                    new_expression, local_change = self._fold(
                        statement.expression,
                    )

                    statement.expression = new_expression

                    changed |= local_change

        return PassResult(
            changed=changed,
        )

    def _fold(
        self,
        expression,
    ):

        if isinstance(expression, IRLiteral):

            return expression, False

        if isinstance(expression, IRUnary):

            operand, changed = self._fold(
                expression.operand,
            )

            expression.operand = operand

            if isinstance(
                operand,
                IRLiteral,
            ):

                value = int(
                    operand.value,
                )

                if expression.operator == "-":

                    return IRLiteral(
                        str(-value),
                    ), True

                if expression.operator == "+":

                    return IRLiteral(
                        str(value),
                    ), True

            return expression, changed

        if isinstance(expression, IRBinary):

            left, left_changed = self._fold(
                expression.left,
            )

            right, right_changed = self._fold(
                expression.right,
            )

            expression.left = left
            expression.right = right

            if (
                isinstance(left, IRLiteral)
                and isinstance(right, IRLiteral)
            ):

                a = int(left.value)
                b = int(right.value)

                if expression.operator == "+":
                    value = a + b

                elif expression.operator == "-":
                    value = a - b

                elif expression.operator == "*":
                    value = a * b

                elif expression.operator == "/":

                    if b == 0:

                        return expression, (
                            left_changed
                            or right_changed
                        )

                    value = a // b

                else:

                    return expression, (
                        left_changed
                        or right_changed
                    )

                return IRLiteral(
                    str(value),
                ), True

            return expression, (
                left_changed
                or right_changed
            )

        return expression, False
