"""
Diagnostic Formatter.
"""


class DiagnosticFormatter:

    def format(
        self,
        diagnostic,
    ):

        lines = []

        lines.append(
            f"{diagnostic.severity}[{diagnostic.code}]"
        )

        if diagnostic.location is not None:

            location = diagnostic.location

            lines.append(
                f"{location.file}:{location.line}:{location.column}"
            )

        lines.append("")

        lines.append(
            diagnostic.message
        )

        if diagnostic.explanation:

            lines.append("")

            lines.append(
                diagnostic.explanation
            )

        if diagnostic.suggestion:

            lines.append("")

            lines.append(
                "Suggestion:"
            )

            lines.append(
                diagnostic.suggestion
            )

        return "\n".join(lines)
