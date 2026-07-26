"""
Focused tests for deterministic validation-engine execution.
"""

from app.domain.specification_ir import SpecificationIR
from app.engines.diagnostics.diagnostic import Diagnostic
from app.engines.diagnostics.diagnostic_severity import DiagnosticSeverity
from app.engines.rule_engine.validation_engine import ValidationEngine
from app.engines.rule_engine.validation_engine_result import (
    ValidationEngineResult,
)
from app.engines.rule_engine.validation_rule import ValidationRule


class FirstRule(ValidationRule):
    rule_id = "RIVA-VAL-TEST-101"
    description = "Produces one warning."

    def _evaluate(
        self,
        specification: SpecificationIR,
    ) -> tuple[Diagnostic, ...]:
        return (
            Diagnostic(
                code="RIVA-VAL-TEST-WARNING",
                message="First diagnostic.",
                severity=DiagnosticSeverity.WARNING,
                stage=self.stage,
            ),
        )


class SecondRule(ValidationRule):
    rule_id = "RIVA-VAL-TEST-102"
    description = "Produces one error and one informational diagnostic."

    def _evaluate(
        self,
        specification: SpecificationIR,
    ) -> tuple[Diagnostic, ...]:
        return (
            Diagnostic(
                code="RIVA-VAL-TEST-ERROR",
                message="Second diagnostic.",
                severity=DiagnosticSeverity.ERROR,
                stage=self.stage,
            ),
            Diagnostic(
                code="RIVA-VAL-TEST-INFO",
                message="Third diagnostic.",
                severity=DiagnosticSeverity.INFO,
                stage=self.stage,
            ),
        )


class DuplicateFirstRule(ValidationRule):
    rule_id = FirstRule.rule_id
    description = "Duplicates the first rule identifier."

    def _evaluate(
        self,
        specification: SpecificationIR,
    ) -> tuple[Diagnostic, ...]:
        return ()


def test_engine_constructor_validates_rules() -> None:
    try:
        ValidationEngine("invalid")  # type: ignore[arg-type]
    except TypeError as error:
        assert "sequence" in str(error)
    else:
        raise AssertionError("string rule collection was accepted")

    try:
        ValidationEngine([object()])  # type: ignore[list-item]
    except TypeError as error:
        assert "ValidationRule" in str(error)
    else:
        raise AssertionError("invalid rule object was accepted")

    try:
        ValidationEngine([FirstRule(), DuplicateFirstRule()])
    except ValueError as error:
        assert str(error) == (
            "duplicate validation rule_id: RIVA-VAL-TEST-101"
        )
    else:
        raise AssertionError("duplicate rule identifier was accepted")


def test_engine_preserves_rule_and_diagnostic_order() -> None:
    engine = ValidationEngine([FirstRule(), SecondRule()])

    result = engine.run(SpecificationIR())

    assert isinstance(result, ValidationEngineResult)
    assert engine.rules[0].rule_id == FirstRule.rule_id
    assert engine.rules[1].rule_id == SecondRule.rule_id
    assert [
        rule_result.rule_id
        for rule_result in result.rule_results
    ] == [
        FirstRule.rule_id,
        SecondRule.rule_id,
    ]
    assert [
        diagnostic.message
        for diagnostic in result.diagnostics
    ] == [
        "First diagnostic.",
        "Second diagnostic.",
        "Third diagnostic.",
    ]


def test_engine_result_counts_are_aggregated() -> None:
    result = ValidationEngine(
        [FirstRule(), SecondRule()]
    ).run(SpecificationIR())

    assert result.executed_rule_count == 2
    assert result.diagnostic_count == 3
    assert result.error_count == 1
    assert result.warning_count == 1
    assert result.info_count == 1
    assert result.has_errors is True
    assert result.is_successful is False


def test_empty_engine_is_successful() -> None:
    result = ValidationEngine(()).run(SpecificationIR())

    assert result.rule_results == ()
    assert result.diagnostics == ()
    assert result.executed_rule_count == 0
    assert result.diagnostic_count == 0
    assert result.is_successful is True


def test_engine_run_validates_input() -> None:
    engine = ValidationEngine(())

    try:
        engine.run(object())  # type: ignore[arg-type]
    except TypeError as error:
        assert str(error) == "specification must be a SpecificationIR"
    else:
        raise AssertionError("invalid specification was accepted")


def test_repeated_engine_runs_are_deterministic_and_independent() -> None:
    engine = ValidationEngine([FirstRule(), SecondRule()])
    specification = SpecificationIR()

    first = engine.run(specification)
    second = engine.run(specification)

    assert first == second
    assert first is not second
    assert first.rule_results is not second.rule_results
    assert first.diagnostics == second.diagnostics
    assert first.diagnostics is not second.diagnostics


def main() -> None:
    tests = (
        test_engine_constructor_validates_rules,
        test_engine_preserves_rule_and_diagnostic_order,
        test_engine_result_counts_are_aggregated,
        test_empty_engine_is_successful,
        test_engine_run_validates_input,
        test_repeated_engine_runs_are_deterministic_and_independent,
    )

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print("\nValidation-engine tests passed.")


if __name__ == "__main__":
    main()
