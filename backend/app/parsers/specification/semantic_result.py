"""
Result contract for specification semantic transformation.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.specification_ir import SpecificationIR
from app.engines.diagnostics.diagnostic import Diagnostic
from app.engines.diagnostics.diagnostic_severity import DiagnosticSeverity


@dataclass(frozen=True, slots=True)
class SpecificationSemanticResult:
    """
    Contains a SpecificationIR and its ordered semantic diagnostics.

    The result container and diagnostic sequence are immutable. The
    SpecificationIR remains a mutable domain object so later verification
    stages can enrich it through explicit pipeline operations.
    """

    specification: SpecificationIR
    diagnostics: tuple[Diagnostic, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.specification, SpecificationIR):
            raise TypeError(
                "specification must be a SpecificationIR."
            )

        if not isinstance(self.diagnostics, tuple):
            raise TypeError(
                "diagnostics must be a tuple of Diagnostic objects."
            )

        for index, diagnostic in enumerate(self.diagnostics):
            if not isinstance(diagnostic, Diagnostic):
                raise TypeError(
                    f"diagnostics[{index}] must be a Diagnostic."
                )

    @property
    def diagnostic_count(self) -> int:
        """
        Return the total number of diagnostics.
        """

        return len(self.diagnostics)

    @property
    def error_count(self) -> int:
        """
        Return the number of error diagnostics.
        """

        return self._count(DiagnosticSeverity.ERROR)

    @property
    def warning_count(self) -> int:
        """
        Return the number of warning diagnostics.
        """

        return self._count(DiagnosticSeverity.WARNING)

    @property
    def info_count(self) -> int:
        """
        Return the number of informational diagnostics.
        """

        return self._count(DiagnosticSeverity.INFO)

    @property
    def has_errors(self) -> bool:
        """
        Return whether the result contains at least one error.
        """

        return self.error_count > 0

    @property
    def is_successful(self) -> bool:
        """
        Return whether semantic transformation completed without errors.
        """

        return not self.has_errors

    def _count(self, severity: DiagnosticSeverity) -> int:
        return sum(
            diagnostic.severity is severity
            for diagnostic in self.diagnostics
        )
