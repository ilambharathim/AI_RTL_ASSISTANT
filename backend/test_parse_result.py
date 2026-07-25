"""
Regression tests for recoverable specification parse results.
"""

from dataclasses import FrozenInstanceError

from app.domain.ast.document_node import DocumentNode
from app.engines.diagnostics.diagnostic import Diagnostic
from app.engines.diagnostics.diagnostic_severity import DiagnosticSeverity
from app.parsers.specification.parse_result import SpecificationParseResult


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


def make_diagnostic(
    code: str,
    severity: DiagnosticSeverity,
    line: int,
) -> Diagnostic:
    return Diagnostic(
        code=code,
        message=f"Diagnostic {code}.",
        severity=severity,
        stage="specification-parser",
        line=line,
        column=1,
        source_file="specification.txt",
    )


def test_empty_result_is_successful() -> None:
    document = DocumentNode(source_file="specification.txt")
    result = SpecificationParseResult(document=document)

    assert result.document is document
    assert result.diagnostics == ()
    assert result.diagnostic_count == 0
    assert result.error_count == 0
    assert result.warning_count == 0
    assert result.info_count == 0
    assert result.has_errors is False
    assert result.is_successful is True


def test_diagnostic_counts_are_correct() -> None:
    document = DocumentNode(source_file="specification.txt")

    diagnostics = (
        make_diagnostic(
            "SPEC-PARSE-001",
            DiagnosticSeverity.ERROR,
            2,
        ),
        make_diagnostic(
            "SPEC-PARSE-002",
            DiagnosticSeverity.WARNING,
            4,
        ),
        make_diagnostic(
            "SPEC-PARSE-003",
            DiagnosticSeverity.ERROR,
            7,
        ),
        make_diagnostic(
            "SPEC-PARSE-004",
            DiagnosticSeverity.INFO,
            9,
        ),
    )

    result = SpecificationParseResult(
        document=document,
        diagnostics=diagnostics,
    )

    assert result.diagnostics is diagnostics
    assert result.diagnostic_count == 4
    assert result.error_count == 2
    assert result.warning_count == 1
    assert result.info_count == 1
    assert result.has_errors is True
    assert result.is_successful is False


def test_diagnostic_order_is_preserved() -> None:
    first = make_diagnostic(
        "SPEC-PARSE-001",
        DiagnosticSeverity.ERROR,
        3,
    )
    second = make_diagnostic(
        "SPEC-PARSE-002",
        DiagnosticSeverity.ERROR,
        8,
    )
    third = make_diagnostic(
        "SPEC-PARSE-003",
        DiagnosticSeverity.WARNING,
        12,
    )

    result = SpecificationParseResult(
        document=DocumentNode(),
        diagnostics=(first, second, third),
    )

    assert result.diagnostics[0] is first
    assert result.diagnostics[1] is second
    assert result.diagnostics[2] is third


def test_warning_only_result_is_successful() -> None:
    warning = make_diagnostic(
        "SPEC-PARSE-010",
        DiagnosticSeverity.WARNING,
        5,
    )

    result = SpecificationParseResult(
        document=DocumentNode(),
        diagnostics=(warning,),
    )

    assert result.diagnostic_count == 1
    assert result.error_count == 0
    assert result.warning_count == 1
    assert result.has_errors is False
    assert result.is_successful is True


def test_result_container_is_immutable() -> None:
    result = SpecificationParseResult(
        document=DocumentNode(),
    )

    assert_raises(
        FrozenInstanceError,
        "cannot assign to field 'diagnostics'",
        lambda: setattr(result, "diagnostics", ()),
    )

    assert_raises(
        FrozenInstanceError,
        "cannot assign to field 'document'",
        lambda: setattr(result, "document", DocumentNode()),
    )


def test_document_type_is_validated() -> None:
    assert_raises(
        TypeError,
        "document must be a DocumentNode.",
        lambda: SpecificationParseResult(
            document="not-a-document",
        ),
    )


def test_diagnostics_container_is_validated() -> None:
    assert_raises(
        TypeError,
        "diagnostics must be a tuple of Diagnostic objects.",
        lambda: SpecificationParseResult(
            document=DocumentNode(),
            diagnostics=[],
        ),
    )


def test_diagnostic_members_are_validated() -> None:
    valid_diagnostic = make_diagnostic(
        "SPEC-PARSE-001",
        DiagnosticSeverity.ERROR,
        1,
    )

    assert_raises(
        TypeError,
        "diagnostics[1] must be a Diagnostic.",
        lambda: SpecificationParseResult(
            document=DocumentNode(),
            diagnostics=(
                valid_diagnostic,
                "not-a-diagnostic",
            ),
        ),
    )


def main() -> None:
    tests = (
        test_empty_result_is_successful,
        test_diagnostic_counts_are_correct,
        test_diagnostic_order_is_preserved,
        test_warning_only_result_is_successful,
        test_result_container_is_immutable,
        test_document_type_is_validated,
        test_diagnostics_container_is_validated,
        test_diagnostic_members_are_validated,
    )

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print("\nSpecificationParseResult tests passed.")


if __name__ == "__main__":
    main()
