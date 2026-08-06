"""
Collects identifier usage throughout the AST.
"""

from app.ast.expression import (
    IdentifierExpression,
    UnaryExpression,
    BinaryExpression,
)


class UsageCollector:

    def collect(
        self,
        syntax_tree,
    ):

        used = set()

        self._visit(
            syntax_tree,
            used,
        )

        return used

    def _visit(
        self,
        node,
        used,
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
                    used,
                )

            return

        if isinstance(
            node,
            IdentifierExpression,
        ):

            used.add(
                node.name,
            )

            return

        if isinstance(
            node,
            UnaryExpression,
        ):

            self._visit(
                node.operand,
                used,
            )

            return

        if isinstance(
            node,
            BinaryExpression,
        ):

            self._visit(
                node.left,
                used,
            )

            self._visit(
                node.right,
                used,
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
                    used,
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
                    used,
                )
