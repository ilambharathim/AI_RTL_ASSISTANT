"""
Control Flow Graph Builder.
"""

from app.analysis.cfg.control_flow_graph import (
    ControlFlowGraph,
)

from app.ast import (
    StatementBlock,
    IfStatement,
)


class CFGBuilder:

    def build(
        self,
        syntax_tree,
    ):

        graph = ControlFlowGraph()

        entry = graph.new_block()

        graph.entry = entry

        current = entry

        current = self._visit(
            syntax_tree,
            graph,
            current,
        )

        exit_block = graph.new_block()

        graph.exit = exit_block

        current.connect(
            exit_block,
        )

        return graph

    def _visit(
        self,
        node,
        graph,
        current,
    ):

        if node is None:
            return current

        #
        # tuple
        #
        if isinstance(
            node,
            tuple,
        ):

            for child in node:

                current = self._visit(

                    child,

                    graph,

                    current,

                )

            return current

        #
        # statement block
        #
        if isinstance(
            node,
            StatementBlock,
        ):

            for statement in node.statements:

                current = self._visit(

                    statement,

                    graph,

                    current,

                )

            return current

        #
        # if statement
        #
        if isinstance(
            node,
            IfStatement,
        ):

            current.statements.append(
                node.condition,
            )

            then_block = graph.new_block()

            merge_block = graph.new_block()

            current.connect(
                then_block,
            )

            then_exit = self._visit(

                node.then_branch,

                graph,

                then_block,

            )

            then_exit.connect(
                merge_block,
            )

            if node.else_branch is not None:

                else_block = graph.new_block()

                current.connect(
                    else_block,
                )

                else_exit = self._visit(

                    node.else_branch,

                    graph,

                    else_block,

                )

                else_exit.connect(
                    merge_block,

                )

            else:

                current.connect(
                    merge_block,
                )

            return merge_block

        #
        # recurse into children
        #
        if hasattr(
            node,
            "__dict__",
        ):

            current.statements.append(
                node,
            )

            return current

        elif hasattr(
            node,
            "__slots__",
        ):

            current.statements.append(
                node,
            )

            return current

        return current
