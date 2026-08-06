"""
Semantic diagnostic rules.
"""

from app.diagnostics import Diagnostic

from app.diagnostics.catalog import (
    RIVA1001,
)


class SemanticRules:

    name = "Semantic Rules"

    def run(
        self,
        semantic_model,
    ):

        diagnostics = []

        for error in getattr(
            semantic_model,
            "identifier_errors",
            [],
        ):

            diagnostics.append(

                Diagnostic(

                    code=RIVA1001.code,

                    category=RIVA1001.category,

                    severity=RIVA1001.severity,

                    message=error,

                    explanation=RIVA1001.explanation,

                    suggestion=RIVA1001.suggestion,

                    repairable=True,

                    confidence=100,

                )

            )

        return diagnostics
