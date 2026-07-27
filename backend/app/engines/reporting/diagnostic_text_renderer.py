"""
Deterministic human-readable rendering for DiagnosticReport.
"""

from app.engines.diagnostics.diagnostic import Diagnostic
from app.engines.reporting.diagnostic_report import DiagnosticReport


class DiagnosticTextRenderer:
    """Render a stable compiler-style plain-text diagnostic report."""

    TITLE = "RIVA Diagnostic Report"

    @classmethod
    def render(cls, report: DiagnosticReport) -> str:
        if not isinstance(report, DiagnosticReport):
            raise TypeError("report must be a DiagnosticReport.")

        lines = [
            cls.TITLE,
            "=" * len(cls.TITLE),
            f"Status: {report.status}",
            (
                "Diagnostics: "
                f"{report.diagnostic_count} "
                f"({report.error_count} errors, "
                f"{report.warning_count} warnings, "
                f"{report.info_count} info)"
            ),
        ]

        if report.diagnostics:
            lines.append("")
            lines.extend(
                cls._render_diagnostic(diagnostic)
                for diagnostic in report.diagnostics
            )

        return "\n".join(lines) + "\n"

    @staticmethod
    def _render_diagnostic(diagnostic: Diagnostic) -> str:
        source = diagnostic.source_file or "<unknown>"
        location = source

        if diagnostic.line > 0:
            location += f":{diagnostic.line}"

            if diagnostic.column > 0:
                location += f":{diagnostic.column}"

        return (
            f"{location}: {diagnostic.severity.value} "
            f"[{diagnostic.code}] "
            f"({diagnostic.stage}) {diagnostic.message}"
        )
