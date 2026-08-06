"""
Combinational Loop Detection.

Detects cycles in the elaborated RTL graph.
"""

from app.diagnostics.base.diagnostic_rule import (
    DiagnosticRule,
)

from app.diagnostics.diagnostic import (
    Diagnostic,
)


class CombinationalLoopRule(DiagnosticRule):

    code = "RIVA4001"

    name = "Combinational Loop"

    def run(
        self,
        semantic_model,
    ):

        diagnostics = []

        elaboration = getattr(
            semantic_model,
            "elaboration",
            None,
        )

        if elaboration is None:
            return diagnostics

        rtl_graph = getattr(
            elaboration,
            "rtl_graph",
            {},
        )

        for module_name, graph in rtl_graph.items():

            adjacency = graph.get(
                "adjacency",
                {},
            )

            visited = set()

            recursion = set()

            for signal in adjacency:

                if self._dfs(
                    signal,
                    adjacency,
                    visited,
                    recursion,
                ):

                    diagnostics.append(

                        Diagnostic(

                            severity="error",

                            code=self.code,

                            message=(
                                f"Combinational loop detected in module "
                                f"'{module_name}' involving signal '{signal}'."
                            ),

                            suggestion=(
                                "Insert sequential storage or remove the feedback path."
                            ),

                        )

                    )

        return diagnostics

    def _dfs(
        self,
        node,
        graph,
        visited,
        recursion,
    ):

        if node in recursion:
            return True

        if node in visited:
            return False

        visited.add(node)

        recursion.add(node)

        for neighbour in graph.get(
            node,
            (),
        ):

            if self._dfs(
                neighbour,
                graph,
                visited,
                recursion,
            ):

                return True

        recursion.remove(
            node,
        )

        return False
