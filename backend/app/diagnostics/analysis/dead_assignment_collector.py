"""
Dead Assignment Collector.

Detects assignments that are overwritten before
their value is ever read.
"""

from app.ast import (
    ProceduralAssignment,
    StatementBlock,
    AlwaysBlock,
    IfStatement,
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
        # IfStatement — branches are mutually exclusive; analyse each
        # branch independently so an assignment in then-branch is never
        # flagged as dead because of an assignment in else-branch.
        #
        if isinstance(node, IfStatement):

            # Visit then-branch with a copy so it can't pollute else-branch.
            then_state = dict(last_assignment)
            self._visit(getattr(node, "then_branch", None), then_state, dead)

            else_state = dict(last_assignment)
            self._visit(getattr(node, "else_branch", None), else_state, dead)

            # After an if/else the set of "live" assignments is the
            # intersection of both branches — only signals assigned in
            # *both* branches can be considered definitely written.
            for signal in set(then_state) | set(else_state):
                node_a = then_state.get(signal)
                node_b = else_state.get(signal)
                # If assigned in both branches, keep the else-branch version
                # as the "last" writer so downstream can detect overwrite.
                if node_a is not None and node_b is not None:
                    last_assignment[signal] = node_b
                elif signal in last_assignment:
                    # Conditionally assigned — don't count the pre-branch
                    # assignment as dead because we may not execute this branch.
                    pass

            return

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
