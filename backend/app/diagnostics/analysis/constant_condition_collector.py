"""
Collect constant conditional expressions.
"""

from app.ast import (
    IfStatement,
)

from app.ast.expression import (
    LiteralExpression,
)


class ConstantConditionCollector:

    def collect(
        self,
        syntax_tree,
    ):

        conditions = []

        self._visit(
            syntax_tree,
            conditions,
        )

        return conditions

    def _visit(
        self,
        node,
        conditions,
    ):

        if node is None:
            return

        if isinstance(
            node,
            tuple,
        ):

            for child in node:

                self._visit(
                    child,
                    conditions,
                )

            return

        if isinstance(
            node,
            IfStatement,
        ):

            if isinstance(
                node.condition,
                LiteralExpression,
            ):

                conditions.append(
                    node,
                )

            self._visit(
                node.then_branch,
                conditions,
            )

            self._visit(
                node.else_branch,
                conditions,
            )

            return

        if hasattr(
            node,
            "__dict__",
        ):

            for value in vars(
                node,
            ).values():

                self._visit(
                    value,
                    conditions,
                )

        elif hasattr(
            node,
            "__slots__",
        ):

            for slot in node.__slots__:

                self._visit(
                    getattr(
                        node,
                        slot,
                        None,
                    ),
                    conditions,
                )
