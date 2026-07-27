"""
Deterministic machine-readable rendering for DiagnosticReport.
"""

import json
from typing import Any

from app.engines.diagnostics.diagnostic import Diagnostic
from app.engines.reporting.diagnostic_report import DiagnosticReport


class DiagnosticJsonRenderer:
    """Render the versioned RIVA diagnostic JSON schema."""

    SCHEMA_VERSION = "1.0"

    @classmethod
    def render(cls, report: DiagnosticReport) -> str:
        if not isinstance(report, DiagnosticReport):
            raise TypeError("report must be a DiagnosticReport.")

        payload = {
            "schema_version": cls.SCHEMA_VERSION,
            "status": report.status,
            "summary": {
                "diagnostic_count": report.diagnostic_count,
                "error_count": report.error_count,
                "warning_count": report.warning_count,
                "info_count": report.info_count,
            },
            "diagnostics": [
                cls._diagnostic_payload(diagnostic)
                for diagnostic in report.diagnostics
            ],
        }

        return json.dumps(
            payload,
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
        ) + "\n"

    @staticmethod
    def _diagnostic_payload(
        diagnostic: Diagnostic,
    ) -> dict[str, Any]:
        return {
            "code": diagnostic.code,
            "message": diagnostic.message,
            "severity": diagnostic.severity.value,
            "stage": diagnostic.stage,
            "source": {
                "file": diagnostic.source_file,
                "line": diagnostic.line,
                "column": diagnostic.column,
            },
        }
