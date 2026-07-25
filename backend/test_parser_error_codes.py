"""
Regression tests for coded specification parser syntax errors.
"""

from app.parsers.specification.exceptions import SpecificationSyntaxError
from app.parsers.specification.parser import SpecificationParser
from app.parsers.specification.parser_diagnostic_code import (
    SpecificationParserDiagnosticCode,
)
from app.parsers.specification.token_types import TokenType
from app.parsers.specification.tokens import Token


def make_token(
    token_type: TokenType,
    value: str,
    *,
    line: int = 1,
    column: int = 1,
    source_file: str = "",
) -> Token:
    return Token(
        type=token_type,
        value=value,
        line=line,
        column=column,
        source_file=source_file,
    )


def assert_syntax_error(
    tokens: tuple[Token, ...],
    expected_code: SpecificationParserDiagnosticCode,
    expected_message: str,
    *,
    expected_line: int = 1,
    expected_column: int = 1,
) -> SpecificationSyntaxError:
    try:
        SpecificationParser(tokens).parse()
    except SpecificationSyntaxError as error:
        assert error.code == expected_code.value
        assert error.message == expected_message
        assert error.line == expected_line
        assert error.column == expected_column
        return error
    else:
        raise AssertionError(
            f"Expected syntax error {expected_code.value}: "
            f"{expected_message}"
        )


def test_unexpected_token_code() -> None:
    error = assert_syntax_error(
        (
            make_token(TokenType.IDENTIFIER, "clk"),
            make_token(TokenType.NEWLINE, "\n", column=4),
            make_token(TokenType.EOF, "", line=2),
        ),
        SpecificationParserDiagnosticCode.UNEXPECTED_TOKEN,
        "Unexpected IDENTIFIER token.",
    )

    assert str(error) == (
        "<memory>:1:1: Unexpected IDENTIFIER token."
    )


def test_section_error_codes() -> None:
    assert_syntax_error(
        (
            make_token(TokenType.SECTION_HEADER, ""),
            make_token(TokenType.NEWLINE, "\n"),
            make_token(TokenType.EOF, "", line=2),
        ),
        SpecificationParserDiagnosticCode.EMPTY_SECTION_HEADER,
        "Section header must not be empty.",
    )

    assert_syntax_error(
        (
            make_token(TokenType.SECTION_HEADER, "Inputs"),
            make_token(TokenType.EOF, "", line=2),
        ),
        (
            SpecificationParserDiagnosticCode
            .EXPECTED_NEWLINE_AFTER_SECTION_HEADER
        ),
        "Expected NEWLINE after section header.",
        expected_line=2,
    )


def test_key_value_error_codes() -> None:
    assert_syntax_error(
        (
            make_token(TokenType.KEY, " "),
            make_token(TokenType.COLON, ":", column=2),
            make_token(TokenType.NEWLINE, "\n", column=3),
            make_token(TokenType.EOF, "", line=2),
        ),
        SpecificationParserDiagnosticCode.EMPTY_KEY,
        "Key must not be empty.",
    )

    assert_syntax_error(
        (
            make_token(TokenType.KEY, "Module Name"),
            make_token(TokenType.VALUE, "mux2to1", column=13),
            make_token(TokenType.NEWLINE, "\n", column=20),
            make_token(TokenType.EOF, "", line=2),
        ),
        SpecificationParserDiagnosticCode.EXPECTED_COLON_AFTER_KEY,
        "Expected COLON after key.",
        expected_column=13,
    )

    assert_syntax_error(
        (
            make_token(TokenType.KEY, "Description"),
            make_token(TokenType.COLON, ":", column=12),
            make_token(TokenType.VALUE, "   ", column=14),
            make_token(TokenType.NEWLINE, "\n", column=17),
            make_token(TokenType.EOF, "", line=2),
        ),
        SpecificationParserDiagnosticCode.EMPTY_VALUE,
        "VALUE token must not be empty.",
        expected_column=14,
    )

    assert_syntax_error(
        (
            make_token(TokenType.KEY, "Module Name"),
            make_token(TokenType.COLON, ":", column=12),
            make_token(TokenType.VALUE, "mux2to1", column=14),
            make_token(TokenType.EOF, "", line=2),
        ),
        (
            SpecificationParserDiagnosticCode
            .EXPECTED_NEWLINE_AFTER_KEY_VALUE
        ),
        "Expected NEWLINE after key-value entry.",
        expected_line=2,
    )


def test_list_item_error_codes() -> None:
    assert_syntax_error(
        (
            make_token(TokenType.LIST_ITEM, "   "),
            make_token(TokenType.NEWLINE, "\n", column=4),
            make_token(TokenType.EOF, "", line=2),
        ),
        SpecificationParserDiagnosticCode.EMPTY_LIST_ITEM,
        "List item must not be empty.",
    )

    assert_syntax_error(
        (
            make_token(TokenType.LIST_ITEM, "clk"),
            make_token(TokenType.EOF, "", line=2),
        ),
        (
            SpecificationParserDiagnosticCode
            .EXPECTED_NEWLINE_AFTER_LIST_ITEM
        ),
        "Expected NEWLINE after list item.",
        expected_line=2,
    )


def test_text_error_codes() -> None:
    assert_syntax_error(
        (
            make_token(TokenType.TEXT, "   "),
            make_token(TokenType.NEWLINE, "\n", column=4),
            make_token(TokenType.EOF, "", line=2),
        ),
        SpecificationParserDiagnosticCode.EMPTY_TEXT,
        "Text must not be empty.",
    )

    assert_syntax_error(
        (
            make_token(TokenType.TEXT, "Requirement text."),
            make_token(TokenType.EOF, "", line=2),
        ),
        SpecificationParserDiagnosticCode.EXPECTED_NEWLINE_AFTER_TEXT,
        "Expected NEWLINE after text.",
        expected_line=2,
    )


def test_error_preserves_source_location_and_text() -> None:
    error = assert_syntax_error(
        (
            make_token(
                TokenType.KEY,
                "Module Name",
                source_file="broken.txt",
            ),
            make_token(
                TokenType.VALUE,
                "mux2to1",
                column=13,
                source_file="broken.txt",
            ),
            make_token(
                TokenType.NEWLINE,
                "\n",
                column=20,
                source_file="broken.txt",
            ),
            make_token(
                TokenType.EOF,
                "",
                line=2,
                source_file="broken.txt",
            ),
        ),
        SpecificationParserDiagnosticCode.EXPECTED_COLON_AFTER_KEY,
        "Expected COLON after key.",
        expected_column=13,
    )

    assert error.source_file == "broken.txt"
    assert str(error) == (
        "broken.txt:1:13: Expected COLON after key."
    )


def test_legacy_constructor_remains_compatible() -> None:
    error = SpecificationSyntaxError(
        "Unexpected token.",
        line=4,
        column=7,
        source_file="legacy.txt",
    )

    assert error.code == (
        SpecificationParserDiagnosticCode.UNEXPECTED_TOKEN.value
    )
    assert error.message == "Unexpected token."
    assert error.line == 4
    assert error.column == 7
    assert error.source_file == "legacy.txt"
    assert str(error) == (
        "legacy.txt:4:7: Unexpected token."
    )


def test_error_rejects_invalid_code_type() -> None:
    try:
        SpecificationSyntaxError(
            "Unexpected token.",
            code="SPEC-PARSE-001",
            line=1,
            column=1,
        )
    except TypeError as error:
        assert str(error) == (
            "code must be a SpecificationParserDiagnosticCode."
        )
    else:
        raise AssertionError(
            "SpecificationSyntaxError must reject untyped codes."
        )


def main() -> None:
    tests = (
        test_unexpected_token_code,
        test_section_error_codes,
        test_key_value_error_codes,
        test_list_item_error_codes,
        test_text_error_codes,
        test_error_preserves_source_location_and_text,
        test_legacy_constructor_remains_compatible,
        test_error_rejects_invalid_code_type,
    )

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print("\nParser error-code tests passed.")


if __name__ == "__main__":
    main()
