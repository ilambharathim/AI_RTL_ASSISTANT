"""
RIVA Diagnostic Engine.

Runs every diagnostic rule and stores the resulting
diagnostics inside the semantic model.
"""

from app.diagnostics.rules.width_rules import (
    WidthRules,
)

from app.diagnostics.rules.semantic_rules import (
    SemanticRules,
)

from app.diagnostics.rules.elaboration_rules import (
    ElaborationRules,
)

from app.diagnostics.rules.lint_rules import (
    LintRules,
)


class DiagnosticEngine:

    def __init__(self):

        self.rules = (

            SemanticRules(),

            WidthRules(),

            ElaborationRules(),

            LintRules(),

        )

    def analyze(
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

        semantic_model.diagnostics = diagnostics

        return diagnostics
