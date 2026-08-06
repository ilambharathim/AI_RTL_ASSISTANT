"""
RTL Graph Builder.

Builds signal dependency graphs used by diagnostics.
"""

from app.ast import (
    ContinuousAssign,
    ProceduralAssignment,
    AlwaysBlock,
    StatementBlock,
    IfStatement,
)

from app.ast.expression import (
    IdentifierExpression,
    UnaryExpression,
    BinaryExpression,
)


class RTLGraphBuilder:

    def build(
        self,
        semantic_model,
    ):

        rtl_graph = {}

        for resolved_module in (
            semantic_model.elaboration.elaborated_modules.values()
        ):

            bound_hierarchy = (
                semantic_model.elaboration.port_bindings
            )

            bound_module = (
                bound_hierarchy.modules.get(
                    resolved_module.name,
                )
            )

            graph = {

                "instances": (
                    bound_module.instances
                    if bound_module is not None
                    else []
                ),

                "adjacency": {},

            }

            self._visit_module(

                resolved_module.declaration,

                graph,

            )

            resolved_module.rtl_graph = graph

            rtl_graph[
                resolved_module.name
            ] = graph

        semantic_model.elaboration.rtl_graph = rtl_graph

    def _visit_module(
        self,
        module,
        graph,
    ):

        for member in module.members:

            self._visit(
                member,
                graph,
            )

    def _visit(
        self,
        node,
        graph,
    ):

        if node is None:
            return

        if isinstance(
            node,
            AlwaysBlock,
        ):

            for statement in node.statements:

                self._visit(
                    statement,
                    graph,
                )

            return

        if isinstance(
            node,
            StatementBlock,
        ):

            for statement in node.statements:

                self._visit(
                    statement,
                    graph,
                )

            return

        if isinstance(
            node,
            IfStatement,
        ):

            self._visit(
                node.then_branch,
                graph,
            )

            self._visit(
                node.else_branch,
                graph,
            )

            return

        if isinstance(
            node,
            (
                ContinuousAssign,
                ProceduralAssignment,
            ),
        ):

            target = node.target

            graph["adjacency"].setdefault(
                target,
                [],
            )

            sources = []

            self._collect_sources(
                node.expression,
                sources,
            )

            graph["adjacency"][
                target
            ].extend(
                sources
            )

    def _collect_sources(
        self,
        expression,
        sources,
    ):

        if expression is None:
            return

        if isinstance(
            expression,
            IdentifierExpression,
        ):

            sources.append(
                expression.name,
            )

            return

        if isinstance(
            expression,
            UnaryExpression,
        ):

            self._collect_sources(
                expression.operand,
                sources,
            )

            return

        if isinstance(
            expression,
            BinaryExpression,
        ):

            self._collect_sources(
                expression.left,
                sources,
            )

            self._collect_sources(
                expression.right,
                sources,
            )
