"""
Typed IR Dead Assignment Elimination.

Removes assignments whose destination is never read.
"""

from app.ir.ir_statement import (
    IRAssignment,
)

from app.ir.ir_expression import (
    IRIdentifier,
    IRBinary,
    IRUnary,
)

from app.optimization.model.pass_result import (
    PassResult,
)


class TypedDeadAssignmentElimination:

    name = "typed_dead_assignment_elimination"

    def run(
        self,
        semantic_model,
        context,
    ):

        changed = False

        for module in semantic_model.elaboration.ir.values():

            used = set()

            #
            # Collect identifiers used in expressions
            #
            for statement in module.statements:

                if hasattr(
                    statement,
                    "expression",
                ):

                    self._collect(
                        statement.expression,
                        used,
                    )

            #
            # Remove dead assignments
            #
            new_statements = []

            for statement in module.statements:

                if isinstance(
                    statement,
                    IRAssignment,
                ):

                    if statement.target not in used:

                        changed = True

                        continue

                new_statements.append(
                    statement,
                )

            module.statements = new_statements

        return PassResult(
            changed=changed,
        )

    def _collect(
        self,
        expression,
        used,
    ):

        if isinstance(
            expression,
            IRIdentifier,
        ):

            used.add(
                expression.name,
            )

            return

        if isinstance(
            expression,
            IRUnary,
        ):

            self._collect(
                expression.operand,
                used,
            )

            return

        if isinstance(
            expression,
            IRBinary,
        ):

            self._collect(
                expression.left,
                used,
            )

            self._collect(
                expression.right,
                used,
            )
