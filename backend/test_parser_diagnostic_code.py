"""
Regression tests for specification parser diagnostic codes.
"""

from app.parsers.specification.parser_diagnostic_code import (
    SpecificationParserDiagnosticCode,
)


EXPECTED_CODES = (
    (
        "UNEXPECTED_TOKEN",
        "SPEC-PARSE-001",
    ),
    (
        "EXPECTED_SECTION_HEADER",
        "SPEC-PARSE-002",
    ),
    (
        "EMPTY_SECTION_HEADER",
        "SPEC-PARSE-003",
    ),
    (
        "EXPECTED_NEWLINE_AFTER_SECTION_HEADER",
        "SPEC-PARSE-004",
    ),
    (
        "EXPECTED_KEY",
        "SPEC-PARSE-005",
    ),
    (
        "EMPTY_KEY",
        "SPEC-PARSE-006",
    ),
    (
        "EXPECTED_COLON_AFTER_KEY",
        "SPEC-PARSE-007",
    ),
    (
        "EMPTY_VALUE",
        "SPEC-PARSE-008",
    ),
    (
        "EXPECTED_NEWLINE_AFTER_KEY_VALUE",
        "SPEC-PARSE-009",
    ),
    (
        "EXPECTED_LIST_ITEM",
        "SPEC-PARSE-010",
    ),
    (
        "EMPTY_LIST_ITEM",
        "SPEC-PARSE-011",
    ),
    (
        "EXPECTED_NEWLINE_AFTER_LIST_ITEM",
        "SPEC-PARSE-012",
    ),
    (
        "EXPECTED_TEXT",
        "SPEC-PARSE-013",
    ),
    (
        "EMPTY_TEXT",
        "SPEC-PARSE-014",
    ),
    (
        "EXPECTED_NEWLINE_AFTER_TEXT",
        "SPEC-PARSE-015",
    ),
)


def test_complete_code_contract_is_stable() -> None:
    actual_codes = tuple(
        (code.name, code.value)
        for code in SpecificationParserDiagnosticCode
    )

    assert actual_codes == EXPECTED_CODES


def test_code_values_are_unique() -> None:
    values = tuple(
        code.value
        for code in SpecificationParserDiagnosticCode
    )

    assert len(values) == len(set(values))


def test_code_values_are_contiguous() -> None:
    expected_values = tuple(
        f"SPEC-PARSE-{number:03d}"
        for number in range(1, 16)
    )

    actual_values = tuple(
        code.value
        for code in SpecificationParserDiagnosticCode
    )

    assert actual_values == expected_values


def test_codes_are_string_compatible() -> None:
    for code in SpecificationParserDiagnosticCode:
        assert isinstance(code, str)
        assert code == code.value
        assert code.startswith("SPEC-PARSE-")


def test_name_lookup_is_stable() -> None:
    for expected_name, expected_value in EXPECTED_CODES:
        code = SpecificationParserDiagnosticCode[expected_name]

        assert code.name == expected_name
        assert code.value == expected_value


def test_value_lookup_is_stable() -> None:
    for expected_name, expected_value in EXPECTED_CODES:
        code = SpecificationParserDiagnosticCode(expected_value)

        assert code.name == expected_name
        assert code.value == expected_value


def test_unknown_name_is_rejected() -> None:
    try:
        SpecificationParserDiagnosticCode["UNKNOWN_CODE"]
    except KeyError as error:
        assert error.args == ("UNKNOWN_CODE",)
    else:
        raise AssertionError("Unknown diagnostic names must be rejected.")


def test_unknown_value_is_rejected() -> None:
    try:
        SpecificationParserDiagnosticCode("SPEC-PARSE-999")
    except ValueError:
        pass
    else:
        raise AssertionError("Unknown diagnostic values must be rejected.")


def main() -> None:
    tests = (
        test_complete_code_contract_is_stable,
        test_code_values_are_unique,
        test_code_values_are_contiguous,
        test_codes_are_string_compatible,
        test_name_lookup_is_stable,
        test_value_lookup_is_stable,
        test_unknown_name_is_rejected,
        test_unknown_value_is_rejected,
    )

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print("\nSpecificationParserDiagnosticCode tests passed.")


if __name__ == "__main__":
    main()
