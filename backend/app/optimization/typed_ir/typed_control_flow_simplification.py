"""
Typed IR Control Flow Simplification.

Removes branches whose condition is a compile-time constant.
"""

from app.ir.ir_statement import (
    IRIf,
    IRBlock,
)

from app.ir.ir_expression import (
    IRLiteral,
)

from app.optimization.model.pass_result import (
    PassResult,
)


class TypedControlFlowSimplification:

    name = "typed_control_flow_simplification"

    def run(
        self,
        semantic_model,
        context,
    ):

        changed = False

        for module in semantic_model.elaboration.ir.values():

            new_statements = []

            for statement in module.statements:

                if isinstance(
                    statement,
                    IRIf,
                ):

                    if isinstance(
                        statement.condition,
                        IRLiteral,
                    ):

                        value = int(
                            statement.condition.value,
                        )

                        changed = True

                        if value:

                            if isinstance(
                                statement.then_branch,
                                IRBlock,
                            ):

                                new_statements.extend(
                                    statement.then_branch.statements
                                )

                            else:

                                new_statements.append(
                                    statement.then_branch
                                )

                        else:

                            if statement.else_branch is not None:

                                if isinstance(
                                    statement.else_branch,
                                    IRBlock,
                                ):

                                    new_statements.extend(
                                        statement.else_branch.statements
                                    )

                                else:

                                    new_statements.append(
                                        statement.else_branch
                                    )

                        continue

                new_statements.append(
                    statement,
                )

            module.statements = new_statements

        return PassResult(
            changed=changed,
        )
