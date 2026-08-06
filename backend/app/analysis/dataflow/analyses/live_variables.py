"""
Live Variable Analysis.

Backward data-flow analysis.
"""

from app.analysis.dataflow import (
    DataFlowAnalysis,
)

from app.ast import (
    ProceduralAssignment,
)

from app.ast.expression import (
    IdentifierExpression,
    UnaryExpression,
    BinaryExpression,
)


class LiveVariableAnalysis(
    DataFlowAnalysis,
):

    forward = False

    def initial(
        self,
    ):

        return set()

    def meet(
        self,
        sets,
    ):

        result = set()

        for value in sets:

            result |= value

        return result

    def transfer(
        self,
        block,
        outgoing,
    ):

        live = set(
            outgoing,
        )

        for statement in reversed(
            block.statements,
        ):

            if isinstance(
                statement,
                ProceduralAssignment,
            ):

                if statement.target in live:

                    live.remove(
                        statement.target,
                    )

                self._collect_reads(

                    statement.expression,

                    live,

                )

        return live

    def _collect_reads(
        self,
        expression,
        live,
    ):

        if expression is None:
            return

        if isinstance(
            expression,
            IdentifierExpression,
        ):

            live.add(
                expression.name,
            )

            return

        if isinstance(
            expression,
            UnaryExpression,
        ):

            self._collect_reads(
                expression.operand,
                live,
            )

            return

        if isinstance(
            expression,
            BinaryExpression,
        ):

            self._collect_reads(
                expression.left,
                live,
            )

            self._collect_reads(
                expression.right,
                live,
            )
