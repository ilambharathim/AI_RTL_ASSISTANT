"""
Immutable diagnostic-report contract for RIVA analysis results.
"""

from collections.abc import Sequence
from dataclasses import dataclass

from app.engines.diagnostics.diagnostic import Diagnostic
from app.engines.diagnostics.diagnostic_severity import DiagnosticSeverity


@dataclass(frozen=True, slots=True)
class DiagnosticReport:
    """
    Ordered diagnostics and deterministic summary information.

    The report does not add timestamps or environment-dependent metadata.
    """

    diagnostics: tuple[Diagnostic, ...] = ()

    def __post_init__(self) -> None:
        if type(self.diagnostics) is not tuple:
            raise TypeError("diagnostics must be a tuple.")

        for diagnostic in self.diagnostics:
            if not isinstance(diagnostic, Diagnostic):
                raise TypeError(
                    "diagnostics must contain only Diagnostic instances."
                )

    @classmethod
    def from_diagnostics(
        cls,
        diagnostics: Sequence[Diagnostic],
    ) -> "DiagnosticReport":
        if isinstance(diagnostics, (str, bytes)) or not isinstance(
            diagnostics,
            Sequence,
        ):
            raise TypeError(
                "diagnostics must be a sequence of Diagnostic instances."
            )

        return cls(diagnostics=tuple(diagnostics))

    @property
    def diagnostic_count(self) -> int:
        return len(self.diagnostics)

    @property
    def error_count(self) -> int:
        return self._count(DiagnosticSeverity.ERROR)

    @property
    def warning_count(self) -> int:
        return self._count(DiagnosticSeverity.WARNING)

    @property
    def info_count(self) -> int:
        return self._count(DiagnosticSeverity.INFO)

    @property
    def has_errors(self) -> bool:
        return self.error_count > 0

    @property
    def is_successful(self) -> bool:
        return not self.has_errors

    @property
    def status(self) -> str:
        return "FAILED" if self.has_errors else "PASSED"

    def _count(self, severity: DiagnosticSeverity) -> int:
        return sum(
            diagnostic.severity is severity
            for diagnostic in self.diagnostics
        )
