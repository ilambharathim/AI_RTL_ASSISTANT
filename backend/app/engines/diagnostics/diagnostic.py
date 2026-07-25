"""
Immutable diagnostic value model for RIVA.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.engines.diagnostics.diagnostic_severity import DiagnosticSeverity


@dataclass(frozen=True, slots=True)
class Diagnostic:
    """
    Represents one deterministic diagnostic emitted by a RIVA stage.

    Line and column use zero when a diagnostic is not tied to an exact source
    location. Source-based diagnostics should use one-based locations.
    """

    code: str
    message: str
    severity: DiagnosticSeverity
    stage: str
    line: int = 0
    column: int = 0
    source_file: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.code, str) or not self.code.strip():
            raise ValueError("code must be a non-empty string.")

        if not isinstance(self.message, str) or not self.message.strip():
            raise ValueError("message must be a non-empty string.")

        if not isinstance(self.severity, DiagnosticSeverity):
            raise TypeError("severity must be a DiagnosticSeverity.")

        if not isinstance(self.stage, str) or not self.stage.strip():
            raise ValueError("stage must be a non-empty string.")

        if type(self.line) is not int or self.line < 0:
            raise ValueError(
                "line must be an integer greater than or equal to 0."
            )

        if type(self.column) is not int or self.column < 0:
            raise ValueError(
                "column must be an integer greater than or equal to 0."
            )

        if not isinstance(self.source_file, str):
            raise TypeError("source_file must be a string.")

    def __str__(self) -> str:
        """
        Return a stable single-line compiler-style representation.
        """

        location = self.source_file or "<memory>"

        if self.line > 0:
            location += f":{self.line}"

        if self.column > 0:
            location += f":{self.column}"

        return (
            f"{location}: {self.severity.value} "
            f"{self.code} [{self.stage}]: {self.message}"
        )
