"""
Dead Assignment Collector.

Detects assignments that are overwritten before
their value is ever read.
"""

from app.ast import (
    ProceduralAssignment,
    StatementBlock,
    AlwaysBlock,
)

from app.ast.expression import (
    IdentifierExpression,
    UnaryExpression,
    BinaryExpression,
)


class DeadAssignmentCollector:

    def collect(
        self,
        syntax_tree,
    ):

        dead = []

        self._visit(
            syntax_tree,
            {},
            dead,
        )

        return dead

    def _visit(
        self,
        node,
        last_assignment,
        dead,
    ):

        if node is None:
            return

        #
        # tuples
        #
        if isinstance(
            node,
            tuple,
        ):

            for child in node:

                self._visit(
                    child,
                    last_assignment,
                    dead,
                )

            return

        #
        # blocks
        #
        if isinstance(
            node,
            (StatementBlock, AlwaysBlock),
        ):

            for statement in node.statements:

                self._visit(
                    statement,
                    last_assignment,
                    dead,
                )

            return

        #
        # assignment
        #
        if isinstance(
            node,
            ProceduralAssignment,
        ):

            self._mark_reads(
                node.expression,
                last_assignment,
            )

            signal = node.target

            if signal in last_assignment:

                dead.append(
                    last_assignment[signal]
                )

            last_assignment[signal] = node

            return

        #
        # recurse
        #
        if hasattr(
            node,
            "__dict__",
        ):

            for value in vars(node).values():

                self._visit(
                    value,
                    last_assignment,
                    dead,
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
                    last_assignment,
                    dead,
                )

    def _mark_reads(
        self,
        expression,
        last_assignment,
    ):

        if expression is None:
            return

        if isinstance(
            expression,
            IdentifierExpression,
        ):

            last_assignment.pop(
                expression.name,
                None,
            )

            return

        if isinstance(
            expression,
            UnaryExpression,
        ):

            self._mark_reads(
                expression.operand,
                last_assignment,
            )

            return

        if isinstance(
            expression,
            BinaryExpression,
        ):

            self._mark_reads(
                expression.left,
                last_assignment,
            )

            self._mark_reads(
                expression.right,
                last_assignment,
            )
