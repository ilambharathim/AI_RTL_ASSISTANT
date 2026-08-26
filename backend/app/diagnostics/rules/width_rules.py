"""
Width diagnostic rules.

Aggregates all width-related diagnostic rules.
"""

from app.diagnostics.rules.width_mismatch import (
    WidthMismatchRule,
)

from app.diagnostics.rules.signedness_mismatch import (
    SignednessMismatchRule,
)


class WidthRules:

    name = "Width Rules"

    def __init__(self):

        self.rules = (
            WidthMismatchRule(),
            SignednessMismatchRule(),
        )

    def run(
        self,
        semantic_model,
    ):

        diagnostics = []

        for rule in self.rules:

            diagnostics.extend(
                rule.run(
                    semantic_model,
                )
            )

        return diagnostics
