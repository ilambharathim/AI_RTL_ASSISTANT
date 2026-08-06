"""
Unused Signal Detection.
"""

from app.diagnostics.base.diagnostic_rule import (
    DiagnosticRule,
)

from app.diagnostics.diagnostic import (
    Diagnostic,
)


class UnusedSignalRule(DiagnosticRule):

    code = "RIVA5001"

    name = "Unused Signal"

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

        for module in rtl_graph.values():

            adjacency = module.get(
                "adjacency",
                {},
            )

            declared = set(
                semantic_model.symbols.keys()
            )

            used = set()

            for sources in adjacency.values():

                used.update(
                    sources
                )

            for signal in declared:

                if signal not in used and signal not in adjacency:

                    diagnostics.append(

                        Diagnostic(

                            severity="warning",

                            code=self.code,

                            message=(
                                f"Signal '{signal}' is declared but never used."
                            ),

                            suggestion=(
                                "Remove the declaration or use the signal."
                            ),

                        )

                    )

        return diagnostics
