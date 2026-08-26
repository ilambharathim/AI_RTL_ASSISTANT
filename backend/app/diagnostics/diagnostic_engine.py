"""
RIVA Diagnostic Engine.

Runs every diagnostic rule and stores the resulting
diagnostics inside the semantic model, performing deterministic
deduplication based on diagnostic identity (code, message, location).
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

        all_diags = list(getattr(semantic_model, "diagnostics", []))

        for rule in self.rules:

            all_diags.extend(

                rule.run(
                    semantic_model,
                )

            )

        deduped = []
        seen = set()

        for d in all_diags:
            key = self._diagnostic_key(d)
            if key not in seen:
                seen.add(key)
                deduped.append(d)

        semantic_model.diagnostics = deduped

        return deduped

    @staticmethod
    def _diagnostic_key(d):
        loc = getattr(d, "location", None)
        source_file = getattr(loc, "source_file", "") if loc else ""
        line = getattr(loc, "line", 0) if loc else 0
        column = getattr(loc, "column", 0) if loc else 0
        code = getattr(d, "code", "")
        message = getattr(d, "message", "")
        return (code, message, source_file, line, column)
