"""
Focused regression tests for specification semantic-stage contracts.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from typing import Callable

from app.domain.specification_ir import SpecificationIR
from app.engines.diagnostics.diagnostic import Diagnostic
from app.engines.diagnostics.diagnostic_severity import DiagnosticSeverity
from app.parsers.specification.semantic_diagnostic_code import (
    SpecificationSemanticDiagnosticCode,
)
from app.parsers.specification.semantic_result import (
    SpecificationSemanticResult,
)


def expect_exception(
    exception_type: type[BaseException],
    message: str,
    operation: Callable[[], object],
) -> None:
    try:
        operation()
    except exception_type as error:
        assert str(error) == message
    else:
        raise AssertionError(
            f"Expected {exception_type.__name__}: {message}"
        )


def make_diagnostic(
    code: SpecificationSemanticDiagnosticCode,
    severity: DiagnosticSeverity,
) -> Diagnostic:
    return Diagnostic(
        code=code.value,
        message=f"Diagnostic for {code.value}.",
        severity=severity,
        stage="specification-semantic-builder",
        source_file="specification.txt",
        line=4,
        column=1,
    )


def test_semantic_codes_are_stable_and_unique() -> None:
    expected_values = (
        "SPEC-SEM-001",
        "SPEC-SEM-002",
        "SPEC-SEM-003",
        "SPEC-SEM-004",
        "SPEC-SEM-005",
        "SPEC-SEM-006",
        "SPEC-SEM-007",
        "SPEC-SEM-008",
        "SPEC-SEM-009",
        "SPEC-SEM-010",
        "SPEC-SEM-011",
        "SPEC-SEM-012",
    )

    actual_values = tuple(
        code.value
        for code in SpecificationSemanticDiagnosticCode
    )

    assert actual_values == expected_values
    assert len(actual_values) == len(set(actual_values))


def test_empty_result_is_successful() -> None:
    specification = SpecificationIR()
    result = SpecificationSemanticResult(specification=specification)

    assert result.specification is specification
    assert result.diagnostics == ()
    assert result.diagnostic_count == 0
    assert result.error_count == 0
    assert result.warning_count == 0
    assert result.info_count == 0
    assert result.has_errors is False
    assert result.is_successful is True


def test_result_counts_ordered_diagnostics() -> None:
    error = make_diagnostic(
        SpecificationSemanticDiagnosticCode.INVALID_PORT_NAME,
        DiagnosticSeverity.ERROR,
    )
    warning = make_diagnostic(
        SpecificationSemanticDiagnosticCode.UNKNOWN_SECTION,
        DiagnosticSeverity.WARNING,
    )
    info = make_diagnostic(
        SpecificationSemanticDiagnosticCode.UNKNOWN_DOCUMENT_ENTRY,
        DiagnosticSeverity.INFO,
    )

    result = SpecificationSemanticResult(
        specification=SpecificationIR(),
        diagnostics=(warning, error, info),
    )

    assert result.diagnostics == (warning, error, info)
    assert result.diagnostic_count == 3
    assert result.error_count == 1
    assert result.warning_count == 1
    assert result.info_count == 1
    assert result.has_errors is True
    assert result.is_successful is False


def test_result_requires_specification_ir() -> None:
    expect_exception(
        TypeError,
        "specification must be a SpecificationIR.",
        lambda: SpecificationSemanticResult(
            specification="invalid"  # type: ignore[arg-type]
        ),
    )


def test_diagnostics_must_be_exact_tuple() -> None:
    expect_exception(
        TypeError,
        "diagnostics must be a tuple of Diagnostic objects.",
        lambda: SpecificationSemanticResult(
            specification=SpecificationIR(),
            diagnostics=[],  # type: ignore[arg-type]
        ),
    )


def test_each_diagnostic_is_validated() -> None:
    expect_exception(
        TypeError,
        "diagnostics[1] must be a Diagnostic.",
        lambda: SpecificationSemanticResult(
            specification=SpecificationIR(),
            diagnostics=(
                make_diagnostic(
                    SpecificationSemanticDiagnosticCode.UNKNOWN_SECTION,
                    DiagnosticSeverity.WARNING,
                ),
                "invalid",  # type: ignore[arg-type]
            ),
        ),
    )


def test_result_container_is_immutable() -> None:
    result = SpecificationSemanticResult(
        specification=SpecificationIR()
    )

    expect_exception(
        FrozenInstanceError,
        "cannot assign to field 'diagnostics'",
        lambda: setattr(result, "diagnostics", ()),
    )


def test_default_diagnostic_tuple_is_shared_safely() -> None:
    first = SpecificationSemanticResult(
        specification=SpecificationIR()
    )
    second = SpecificationSemanticResult(
        specification=SpecificationIR()
    )

    assert first.diagnostics == ()
    assert second.diagnostics == ()
    assert first.diagnostics is second.diagnostics


def main() -> None:
    tests = (
        test_semantic_codes_are_stable_and_unique,
        test_empty_result_is_successful,
        test_result_counts_ordered_diagnostics,
        test_result_requires_specification_ir,
        test_diagnostics_must_be_exact_tuple,
        test_each_diagnostic_is_validated,
        test_result_container_is_immutable,
        test_default_diagnostic_tuple_is_shared_safely,
    )

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print("\nSemantic contract tests passed.")


if __name__ == "__main__":
    main()
