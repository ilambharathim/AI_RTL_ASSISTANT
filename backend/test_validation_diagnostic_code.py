"""
Focused tests for the stable validation diagnostic-code catalog.
"""

from app.engines.rule_engine.validation_diagnostic_code import (
    SpecificationValidationDiagnosticCode,
)


def test_validation_diagnostic_codes_are_stable() -> None:
    assert SpecificationValidationDiagnosticCode.MISSING_PROJECT_NAME.value == (
        "SPEC-VAL-001"
    )
    assert SpecificationValidationDiagnosticCode.MISSING_MODULE_NAME.value == (
        "SPEC-VAL-002"
    )
    assert SpecificationValidationDiagnosticCode.MISSING_PORTS.value == (
        "SPEC-VAL-003"
    )
    assert SpecificationValidationDiagnosticCode.MISSING_REQUIREMENTS.value == (
        "SPEC-VAL-004"
    )
    assert (
        SpecificationValidationDiagnosticCode.INVALID_PORT_DIRECTION.value
        == "SPEC-VAL-005"
    )
    assert SpecificationValidationDiagnosticCode.INVALID_PORT_WIDTH.value == (
        "SPEC-VAL-006"
    )
    assert SpecificationValidationDiagnosticCode.DUPLICATE_PORT_NAME.value == (
        "SPEC-VAL-007"
    )
    assert (
        SpecificationValidationDiagnosticCode.DUPLICATE_REQUIREMENT_ID.value
        == "SPEC-VAL-008"
    )
    assert (
        SpecificationValidationDiagnosticCode.EMPTY_REQUIREMENT_DESCRIPTION.value
        == "SPEC-VAL-009"
    )


def test_validation_diagnostic_codes_are_unique() -> None:
    values = [
        diagnostic_code.value
        for diagnostic_code in SpecificationValidationDiagnosticCode
    ]

    assert len(values) == 9
    assert len(values) == len(set(values))


def test_validation_diagnostic_codes_are_strings() -> None:
    for diagnostic_code in SpecificationValidationDiagnosticCode:
        assert isinstance(diagnostic_code, str)
        assert diagnostic_code.value.startswith("SPEC-VAL-")


def test_validation_diagnostic_code_iteration_order_is_stable() -> None:
    assert [
        diagnostic_code.value
        for diagnostic_code in SpecificationValidationDiagnosticCode
    ] == [
        "SPEC-VAL-001",
        "SPEC-VAL-002",
        "SPEC-VAL-003",
        "SPEC-VAL-004",
        "SPEC-VAL-005",
        "SPEC-VAL-006",
        "SPEC-VAL-007",
        "SPEC-VAL-008",
        "SPEC-VAL-009",
    ]


def main() -> None:
    tests = (
        test_validation_diagnostic_codes_are_stable,
        test_validation_diagnostic_codes_are_unique,
        test_validation_diagnostic_codes_are_strings,
        test_validation_diagnostic_code_iteration_order_is_stable,
    )

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print("\nValidation diagnostic-code tests passed.")


if __name__ == "__main__":
    main()
