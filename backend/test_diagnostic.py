"""
Regression tests for the RIVA diagnostic value model.
"""

from dataclasses import FrozenInstanceError

from app.engines.diagnostics.diagnostic import Diagnostic
from app.engines.diagnostics.diagnostic_severity import DiagnosticSeverity


def assert_raises(
    expected_exception: type[Exception],
    expected_message: str,
    operation,
) -> Exception:
    try:
        operation()
    except expected_exception as error:
        assert str(error) == expected_message
        return error
    else:
        raise AssertionError(
            f"Expected {expected_exception.__name__}: {expected_message}"
        )


def test_severity_values_are_stable() -> None:
    assert DiagnosticSeverity.ERROR.value == "ERROR"
    assert DiagnosticSeverity.WARNING.value == "WARNING"
    assert DiagnosticSeverity.INFO.value == "INFO"

    assert isinstance(DiagnosticSeverity.ERROR, str)


def test_complete_diagnostic_contract() -> None:
    diagnostic = Diagnostic(
        code="SPEC-PARSE-001",
        message="Expected COLON after key.",
        severity=DiagnosticSeverity.ERROR,
        stage="specification-parser",
        line=7,
        column=13,
        source_file="broken.txt",
    )

    assert diagnostic.code == "SPEC-PARSE-001"
    assert diagnostic.message == "Expected COLON after key."
    assert diagnostic.severity is DiagnosticSeverity.ERROR
    assert diagnostic.stage == "specification-parser"
    assert diagnostic.line == 7
    assert diagnostic.column == 13
    assert diagnostic.source_file == "broken.txt"

    assert str(diagnostic) == (
        "broken.txt:7:13: ERROR SPEC-PARSE-001 "
        "[specification-parser]: Expected COLON after key."
    )


def test_optional_source_locations() -> None:
    memory_diagnostic = Diagnostic(
        code="RIVA-INFO-001",
        message="Processing started.",
        severity=DiagnosticSeverity.INFO,
        stage="orchestrator",
    )

    assert str(memory_diagnostic) == (
        "<memory>: INFO RIVA-INFO-001 "
        "[orchestrator]: Processing started."
    )

    line_diagnostic = Diagnostic(
        code="SPEC-WARN-001",
        message="Section is empty.",
        severity=DiagnosticSeverity.WARNING,
        stage="specification-parser",
        line=4,
    )

    assert str(line_diagnostic) == (
        "<memory>:4: WARNING SPEC-WARN-001 "
        "[specification-parser]: Section is empty."
    )


def test_diagnostic_is_immutable() -> None:
    diagnostic = Diagnostic(
        code="SPEC-PARSE-002",
        message="Unexpected token.",
        severity=DiagnosticSeverity.ERROR,
        stage="specification-parser",
    )

    assert_raises(
        FrozenInstanceError,
        "cannot assign to field 'message'",
        lambda: setattr(diagnostic, "message", "changed"),
    )


def test_required_text_fields_are_validated() -> None:
    assert_raises(
        ValueError,
        "code must be a non-empty string.",
        lambda: Diagnostic(
            code="",
            message="message",
            severity=DiagnosticSeverity.ERROR,
            stage="parser",
        ),
    )

    assert_raises(
        ValueError,
        "message must be a non-empty string.",
        lambda: Diagnostic(
            code="CODE",
            message="   ",
            severity=DiagnosticSeverity.ERROR,
            stage="parser",
        ),
    )

    assert_raises(
        ValueError,
        "stage must be a non-empty string.",
        lambda: Diagnostic(
            code="CODE",
            message="message",
            severity=DiagnosticSeverity.ERROR,
            stage="",
        ),
    )


def test_types_and_locations_are_validated() -> None:
    assert_raises(
        TypeError,
        "severity must be a DiagnosticSeverity.",
        lambda: Diagnostic(
            code="CODE",
            message="message",
            severity="ERROR",
            stage="parser",
        ),
    )

    assert_raises(
        ValueError,
        "line must be an integer greater than or equal to 0.",
        lambda: Diagnostic(
            code="CODE",
            message="message",
            severity=DiagnosticSeverity.ERROR,
            stage="parser",
            line=-1,
        ),
    )

    assert_raises(
        ValueError,
        "column must be an integer greater than or equal to 0.",
        lambda: Diagnostic(
            code="CODE",
            message="message",
            severity=DiagnosticSeverity.ERROR,
            stage="parser",
            column=-1,
        ),
    )

    assert_raises(
        TypeError,
        "source_file must be a string.",
        lambda: Diagnostic(
            code="CODE",
            message="message",
            severity=DiagnosticSeverity.ERROR,
            stage="parser",
            source_file=None,
        ),
    )


def main() -> None:
    tests = (
        test_severity_values_are_stable,
        test_complete_diagnostic_contract,
        test_optional_source_locations,
        test_diagnostic_is_immutable,
        test_required_text_fields_are_validated,
        test_types_and_locations_are_validated,
    )

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print("\nDiagnostic model tests passed.")


if __name__ == "__main__":
    main()
