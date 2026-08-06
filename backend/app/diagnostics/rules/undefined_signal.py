"""
Undefined Signal Rule.
"""

from app.diagnostics.base.diagnostic_rule import (
    DiagnosticRule,
)

from app.diagnostics.diagnostic import (
    Diagnostic,
)


class UndefinedSignalRule(DiagnosticRule):

    code = "RIVA1001"

    name = "Undefined Signal"

    def run(
        self,
        semantic_model,
    ):

        diagnostics = []

        errors = getattr(
            semantic_model,
            "identifier_errors",
            (),
        )

        for error in errors:

            diagnostics.append(

                Diagnostic(

                    severity="error",

                    code=self.code,

                    message=error,

                    suggestion=(
                        "Declare the signal before it is used."
                    ),

                )

            )

        return diagnostics
