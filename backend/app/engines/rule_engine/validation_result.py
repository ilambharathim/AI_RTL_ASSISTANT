"""
Deterministic validation-rule result contract.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.engines.diagnostics.diagnostic import Diagnostic
from app.engines.diagnostics.diagnostic_severity import DiagnosticSeverity


@dataclass(frozen=True, slots=True)
class ValidationRuleResult:
    """
    Immutable diagnostics produced by one validation rule execution.
    """

    rule_id: str
    diagnostics: tuple[Diagnostic, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.rule_id, str):
            raise TypeError("rule_id must be a string")

        if not self.rule_id.strip():
            raise ValueError("rule_id must not be empty")

        if type(self.diagnostics) is not tuple:
            raise TypeError("diagnostics must be a tuple")

        for diagnostic in self.diagnostics:
            if not isinstance(diagnostic, Diagnostic):
                raise TypeError(
                    "diagnostics must contain only Diagnostic objects"
                )

    @property
    def diagnostic_count(self) -> int:
        return len(self.diagnostics)

    @property
    def error_count(self) -> int:
        return sum(
            diagnostic.severity is DiagnosticSeverity.ERROR
            for diagnostic in self.diagnostics
        )

    @property
    def warning_count(self) -> int:
        return sum(
            diagnostic.severity is DiagnosticSeverity.WARNING
            for diagnostic in self.diagnostics
        )

    @property
    def info_count(self) -> int:
        return sum(
            diagnostic.severity is DiagnosticSeverity.INFO
            for diagnostic in self.diagnostics
        )

    @property
    def has_errors(self) -> bool:
        return self.error_count > 0

    @property
    def is_successful(self) -> bool:
        return not self.has_errors
