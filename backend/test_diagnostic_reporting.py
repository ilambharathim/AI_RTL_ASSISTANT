"""
Focused tests for deterministic diagnostic reports and renderers.
"""

import json
from dataclasses import FrozenInstanceError

from app.engines.diagnostics.diagnostic import Diagnostic
from app.engines.diagnostics.diagnostic_severity import DiagnosticSeverity
from app.engines.reporting.diagnostic_json_renderer import (
    DiagnosticJsonRenderer,
)
from app.engines.reporting.diagnostic_report import DiagnosticReport
from app.engines.reporting.diagnostic_text_renderer import (
    DiagnosticTextRenderer,
)


def _diagnostics() -> tuple[Diagnostic, ...]:
    return (
        Diagnostic(
            code="SPEC-PARSE-001",
            message="Unexpected token.",
            severity=DiagnosticSeverity.ERROR,
            stage="specification-parser",
            source_file="specification.txt",
            line=4,
            column=2,
        ),
        Diagnostic(
            code="SPEC-VAL-001",
            message="Specification project name is missing.",
            severity=DiagnosticSeverity.WARNING,
            stage="specification-validation",
            source_file="specification.txt",
        ),
        Diagnostic(
            code="SPEC-SEM-001",
            message="Unknown document entry.",
            severity=DiagnosticSeverity.INFO,
            stage="specification-semantic-builder",
        ),
    )


def test_report_contract_counts_and_immutability() -> None:
    report = DiagnosticReport(diagnostics=_diagnostics())

    assert report.diagnostic_count == 3
    assert report.error_count == 1
    assert report.warning_count == 1
    assert report.info_count == 1
    assert report.has_errors
    assert not report.is_successful
    assert report.status == "FAILED"

    try:
        report.diagnostics = ()
    except FrozenInstanceError:
        pass
    else:
        raise AssertionError("DiagnosticReport must be immutable.")


def test_report_constructor_and_factory_validate_inputs() -> None:
    try:
        DiagnosticReport(diagnostics=[])
    except TypeError as error:
        assert str(error) == "diagnostics must be a tuple."
    else:
        raise AssertionError("A non-tuple diagnostics value must fail.")

    try:
        DiagnosticReport.from_diagnostics("invalid")
    except TypeError as error:
        assert str(error) == (
            "diagnostics must be a sequence of Diagnostic instances."
        )
    else:
        raise AssertionError("String diagnostics input must fail.")

    try:
        DiagnosticReport(diagnostics=(object(),))
    except TypeError as error:
        assert str(error) == (
            "diagnostics must contain only Diagnostic instances."
        )
    else:
        raise AssertionError("Invalid diagnostic items must fail.")


def test_empty_report_is_successful() -> None:
    report = DiagnosticReport()

    assert report.diagnostics == ()
    assert report.diagnostic_count == 0
    assert report.status == "PASSED"
    assert report.is_successful
    assert not report.has_errors


def test_text_renderer_is_exact_and_deterministic() -> None:
    report = DiagnosticReport.from_diagnostics(_diagnostics())

    expected = """RIVA Diagnostic Report
======================
Status: FAILED
Diagnostics: 3 (1 errors, 1 warnings, 1 info)

specification.txt:4:2: ERROR [SPEC-PARSE-001] (specification-parser) Unexpected token.
specification.txt: WARNING [SPEC-VAL-001] (specification-validation) Specification project name is missing.
<unknown>: INFO [SPEC-SEM-001] (specification-semantic-builder) Unknown document entry.
"""

    first = DiagnosticTextRenderer.render(report)
    second = DiagnosticTextRenderer.render(report)

    assert first == expected
    assert second == expected


def test_json_renderer_is_versioned_ordered_and_deterministic() -> None:
    report = DiagnosticReport.from_diagnostics(_diagnostics())

    first = DiagnosticJsonRenderer.render(report)
    second = DiagnosticJsonRenderer.render(report)
    payload = json.loads(first)

    assert first == second
    assert first.endswith("\n")
    assert payload["schema_version"] == "1.0"
    assert payload["status"] == "FAILED"
    assert payload["summary"] == {
        "diagnostic_count": 3,
        "error_count": 1,
        "warning_count": 1,
        "info_count": 1,
    }
    assert [
        diagnostic["code"]
        for diagnostic in payload["diagnostics"]
    ] == [
        "SPEC-PARSE-001",
        "SPEC-VAL-001",
        "SPEC-SEM-001",
    ]
    assert payload["diagnostics"][0]["source"] == {
        "file": "specification.txt",
        "line": 4,
        "column": 2,
    }


def test_renderers_validate_report_input() -> None:
    for renderer in (
        DiagnosticTextRenderer,
        DiagnosticJsonRenderer,
    ):
        try:
            renderer.render(object())
        except TypeError as error:
            assert str(error) == "report must be a DiagnosticReport."
        else:
            raise AssertionError("Invalid report input must fail.")


def main() -> None:
    tests = (
        test_report_contract_counts_and_immutability,
        test_report_constructor_and_factory_validate_inputs,
        test_empty_report_is_successful,
        test_text_renderer_is_exact_and_deterministic,
        test_json_renderer_is_versioned_ordered_and_deterministic,
        test_renderers_validate_report_input,
    )

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print("\nDiagnostic-reporting tests passed.")


if __name__ == "__main__":
    main()
