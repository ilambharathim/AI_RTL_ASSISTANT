"""
Width diagnostic rules.

Aggregates all width-related diagnostic rules.
"""

from app.diagnostics.rules.width_mismatch import (
    WidthMismatchRule,
)


class WidthRules:

    name = "Width Rules"

    def __init__(self):

        self.rules = (
            WidthMismatchRule(),
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
