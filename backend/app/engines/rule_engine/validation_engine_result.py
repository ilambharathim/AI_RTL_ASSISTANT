"""
Aggregate result contract for deterministic validation execution.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.engines.diagnostics.diagnostic import Diagnostic
from app.engines.diagnostics.diagnostic_severity import DiagnosticSeverity
from app.engines.rule_engine.validation_result import ValidationRuleResult


@dataclass(frozen=True, slots=True)
class ValidationEngineResult:
    """
    Immutable ordered results produced by a validation-engine run.
    """

    rule_results: tuple[ValidationRuleResult, ...] = ()

    def __post_init__(self) -> None:
        if type(self.rule_results) is not tuple:
            raise TypeError("rule_results must be a tuple")

        for result in self.rule_results:
            if not isinstance(result, ValidationRuleResult):
                raise TypeError(
                    "rule_results must contain only "
                    "ValidationRuleResult objects"
                )

    @property
    def executed_rule_count(self) -> int:
        return len(self.rule_results)

    @property
    def diagnostics(self) -> tuple[Diagnostic, ...]:
        return tuple(
            diagnostic
            for result in self.rule_results
            for diagnostic in result.diagnostics
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
