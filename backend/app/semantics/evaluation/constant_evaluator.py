"""
Constant evaluation pass.

Evaluates parameter expressions and stores the resulting
constant values in the semantic model.
"""

from app.ast import (
    ParameterDeclaration,
)

from app.ast.expression import (
    LiteralExpression,
    IdentifierExpression,
    BinaryExpression,
)


class ConstantEvaluator:

    def evaluate(
        self,
        syntax_tree,
        semantic_model,
    ):

        for declaration in syntax_tree.declarations:

            self._visit(
                declaration,
                semantic_model,
            )

    def _visit(
        self,
        node,
        semantic_model,
    ):

        #
        # Recurse into module members
        #
        if hasattr(
            node,
            "members",
        ):

            for member in node.members:

                self._visit(
                    member,
                    semantic_model,
                )

            return

        #
        # Parameter
        #
        if isinstance(
            node,
            ParameterDeclaration,
        ):

            value = self._evaluate(
                node.value,
                semantic_model,
            )

            if value is not None:

                semantic_model.constant_values[
                    node.name
                ] = value

    def _evaluate(
        self,
        expression,
        semantic_model,
    ):

        if isinstance(
            expression,
            LiteralExpression,
        ):

            if expression.value.isdigit():

                return int(
                    expression.value,
                )

            return None

        if isinstance(
            expression,
            IdentifierExpression,
        ):

            return semantic_model.constant_values.get(
                expression.name,
            )

        if isinstance(
            expression,
            BinaryExpression,
        ):

            left = self._evaluate(
                expression.left,
                semantic_model,
            )

            right = self._evaluate(
                expression.right,
                semantic_model,
            )

            if (
                left is None
                or right is None
            ):

                return None

            if expression.operator == "+":
                return left + right

            if expression.operator == "-":
                return left - right

            if expression.operator == "*":
                return left * right

            if expression.operator == "/":

                if right == 0:
                    return None

                return left // right

        return None

