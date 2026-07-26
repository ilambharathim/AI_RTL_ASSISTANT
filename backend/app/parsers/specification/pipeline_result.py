"""
Immutable result contract for the validated specification pipeline.
"""

from dataclasses import dataclass

from app.domain.specification_ir import SpecificationIR
from app.engines.diagnostics.diagnostic import Diagnostic
from app.engines.diagnostics.diagnostic_severity import DiagnosticSeverity
from app.engines.rule_engine.validation_engine_result import (
    ValidationEngineResult,
)
from app.parsers.specification.parse_result import SpecificationParseResult
from app.parsers.specification.semantic_result import SpecificationSemanticResult


@dataclass(frozen=True, slots=True)
class SpecificationPipelineResult:
    """
    Complete deterministic result for specification analysis.

    Diagnostic ordering is stable by compiler phase:
    parser, semantic builder, then validation engine.
    """

    parse_result: SpecificationParseResult
    semantic_result: SpecificationSemanticResult
    validation_result: ValidationEngineResult

    def __post_init__(self) -> None:
        if not isinstance(self.parse_result, SpecificationParseResult):
            raise TypeError(
                "parse_result must be a SpecificationParseResult."
            )

        if not isinstance(
            self.semantic_result,
            SpecificationSemanticResult,
        ):
            raise TypeError(
                "semantic_result must be a SpecificationSemanticResult."
            )

        if not isinstance(
            self.validation_result,
            ValidationEngineResult,
        ):
            raise TypeError(
                "validation_result must be a ValidationEngineResult."
            )

    @property
    def specification(self) -> SpecificationIR:
        return self.semantic_result.specification

    @property
    def diagnostics(self) -> tuple[Diagnostic, ...]:
        return (
            self.parse_result.diagnostics
            + self.semantic_result.diagnostics
            + self.validation_result.diagnostics
        )

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

    def _count(self, severity: DiagnosticSeverity) -> int:
        return sum(
            diagnostic.severity is severity
            for diagnostic in self.diagnostics
        )
