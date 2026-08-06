"""
Base class for all RIVA diagnostic rules.
"""


class DiagnosticRule:

    code = "RIVA0000"

    name = "Diagnostic Rule"

    def run(
        self,
        semantic_model,
    ):

        raise NotImplementedError
