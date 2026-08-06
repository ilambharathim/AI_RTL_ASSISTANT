"""
Width inference pass.

Determines the bit width of declarations and expressions.
"""

from app.ast import (
    SignalDeclaration,
    ParameterDeclaration,
)

from app.ast.expression import (
    LiteralExpression,
    IdentifierExpression,
    BinaryExpression,
)

from app.semantics.symbols.symbol_info import SymbolInfo


class WidthInference:

    def infer(
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
        # Signal declaration
        #
        if isinstance(
            node,
            SignalDeclaration,
        ):

            width = 1

            if node.packed_range is not None:

                width = self._packed_width(
                    node.packed_range,
                    semantic_model,
                )

            semantic_model.symbols[
                node.name
            ] = SymbolInfo(

                name=node.name,

                symbol_type=node.signal_type,

                width=width,

                declaration=node,

            )

            return

        #
        # Parameter declaration
        #
        if isinstance(
            node,
            ParameterDeclaration,
        ):

            semantic_model.symbols[
                node.name
            ] = SymbolInfo(

                name=node.name,

                symbol_type="parameter",

                width=32,

                declaration=node,

            )

            return

    def _packed_width(
        self,
        packed_range,
        semantic_model,
    ):

        left = self._evaluate(
            packed_range.left,
            semantic_model,
        )

        right = self._evaluate(
            packed_range.right,
            semantic_model,
        )

        if (
            isinstance(left, int)
            and isinstance(right, int)
        ):

            return abs(
                left - right
            ) + 1

        return None

    def _evaluate(
        self,
        expression,
        semantic_model,
    ):

        #
        # Integer literal
        #
        if isinstance(
            expression,
            LiteralExpression,
        ):

            if expression.value.isdigit():

                return int(
                    expression.value,
                )

        #
        # Constant identifier
        #
        if isinstance(
            expression,
            IdentifierExpression,
        ):

            return semantic_model.constant_values.get(
                expression.name,
            )

        #
        # Constant binary expression
        #
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

