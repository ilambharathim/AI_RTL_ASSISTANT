"""
Typed IR Constant Propagation.

Propagates compile-time constants through the Typed IR.
"""

from app.ir.ir_expression import (
    IRIdentifier,
    IRLiteral,
    IRBinary,
    IRUnary,
)

from app.optimization.model.pass_result import PassResult


class TypedConstantPropagation:

    name = "typed_constant_propagation"

    def run(
        self,
        semantic_model,
        context,
    ):

        changed = False

        constants = dict(
            semantic_model.constant_values,
        )

        for module in (
            semantic_model.elaboration.ir.values()
        ):

            for statement in module.statements:

                if hasattr(
                    statement,
                    "expression",
                ):

                    new_expression = self._propagate(

                        statement.expression,

                        constants,

                    )

                    if new_expression is not statement.expression:

                        statement.expression = new_expression

                        changed = True

        return PassResult(
            changed=changed,
        )

    def _propagate(
        self,
        expression,
        constants,
    ):

        if isinstance(
            expression,
            IRIdentifier,
        ):

            if expression.name in constants:

                return IRLiteral(
                    str(
                        constants[
                            expression.name
                        ]
                    )
                )

            return expression

        if isinstance(
            expression,
            IRUnary,
        ):

            expression.operand = self._propagate(
                expression.operand,
                constants,
            )

            return expression

        if isinstance(
            expression,
            IRBinary,
        ):

            expression.left = self._propagate(
                expression.left,
                constants,
            )

            expression.right = self._propagate(
                expression.right,
                constants,
            )

            return expression

        return expression
