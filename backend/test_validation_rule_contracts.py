"""
Focused tests for deterministic validation-rule contracts.
"""

from dataclasses import FrozenInstanceError

from app.domain.specification_ir import SpecificationIR
from app.engines.diagnostics.diagnostic import Diagnostic
from app.engines.diagnostics.diagnostic_severity import DiagnosticSeverity
from app.engines.rule_engine.validation_result import ValidationRuleResult
from app.engines.rule_engine.validation_rule import ValidationRule


class NoOpRule(ValidationRule):
    rule_id = "RIVA-VAL-TEST-001"
    description = "Produces no diagnostics."

    def _evaluate(
        self,
        specification: SpecificationIR,
    ) -> tuple[Diagnostic, ...]:
        return ()


class ErrorRule(ValidationRule):
    rule_id = "RIVA-VAL-TEST-002"
    description = "Produces one deterministic error."

    def _evaluate(
        self,
        specification: SpecificationIR,
    ) -> tuple[Diagnostic, ...]:
        return (
            Diagnostic(
                code="RIVA-VAL-TEST-ERROR",
                message="Deterministic validation failure.",
                severity=DiagnosticSeverity.ERROR,
                stage=self.stage,
            ),
        )


def test_concrete_rule_metadata_is_required() -> None:
    try:
        class MissingRuleId(ValidationRule):
            description = "Invalid rule."

            def _evaluate(
                self,
                specification: SpecificationIR,
            ) -> tuple[Diagnostic, ...]:
                return ()
    except TypeError as error:
        assert "rule_id" in str(error)
    else:
        raise AssertionError("missing rule_id was accepted")

    try:
        class MissingDescription(ValidationRule):
            rule_id = "RIVA-VAL-TEST-003"

            def _evaluate(
                self,
                specification: SpecificationIR,
            ) -> tuple[Diagnostic, ...]:
                return ()
    except TypeError as error:
        assert "description" in str(error)
    else:
        raise AssertionError("missing description was accepted")


def test_rule_run_validates_input_and_returns_result() -> None:
    rule = NoOpRule()
    specification = SpecificationIR()

    result = rule.run(specification)

    assert result == ValidationRuleResult(
        rule_id=NoOpRule.rule_id,
        diagnostics=(),
    )
    assert result.diagnostic_count == 0
    assert result.is_successful is True

    try:
        rule.run(object())  # type: ignore[arg-type]
    except TypeError as error:
        assert str(error) == "specification must be a SpecificationIR"
    else:
        raise AssertionError("invalid specification was accepted")


def test_rule_result_counts_and_immutability() -> None:
    result = ErrorRule().run(SpecificationIR())

    assert result.rule_id == ErrorRule.rule_id
    assert result.diagnostic_count == 1
    assert result.error_count == 1
    assert result.warning_count == 0
    assert result.info_count == 0
    assert result.has_errors is True
    assert result.is_successful is False

    try:
        result.rule_id = "changed"  # type: ignore[misc]
    except FrozenInstanceError:
        pass
    else:
        raise AssertionError("ValidationRuleResult was mutable")


def test_rule_output_contract_is_enforced() -> None:
    try:
        class ListReturningRule(ValidationRule):
            rule_id = "RIVA-VAL-TEST-004"
            description = "Returns an invalid list."

            def _evaluate(self, specification: SpecificationIR):
                return []

        ListReturningRule().run(SpecificationIR())
    except TypeError as error:
        assert "tuple of Diagnostic" in str(error)
    else:
        raise AssertionError("list output was accepted")

    try:
        class WrongStageRule(ValidationRule):
            rule_id = "RIVA-VAL-TEST-005"
            description = "Returns a diagnostic with the wrong stage."

            def _evaluate(
                self,
                specification: SpecificationIR,
            ) -> tuple[Diagnostic, ...]:
                return (
                    Diagnostic(
                        code="RIVA-VAL-TEST-WRONG-STAGE",
                        message="Wrong stage.",
                        severity=DiagnosticSeverity.WARNING,
                        stage="other-stage",
                    ),
                )

        WrongStageRule().run(SpecificationIR())
    except ValueError as error:
        assert "rule stage" in str(error)
    else:
        raise AssertionError("wrong diagnostic stage was accepted")


def test_repeated_rule_runs_are_deterministic() -> None:
    rule = ErrorRule()
    specification = SpecificationIR()

    first = rule.run(specification)
    second = rule.run(specification)

    assert first == second
    assert first is not second
    assert first.diagnostics is not second.diagnostics


def main() -> None:
    tests = (
        test_concrete_rule_metadata_is_required,
        test_rule_run_validates_input_and_returns_result,
        test_rule_result_counts_and_immutability,
        test_rule_output_contract_is_enforced,
        test_repeated_rule_runs_are_deterministic,
    )

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print("\nValidation-rule contract tests passed.")


if __name__ == "__main__":
    main()
