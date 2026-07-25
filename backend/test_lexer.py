"""
Regression tests for the RIVA specification document lexer.
"""

from contextlib import redirect_stdout
from io import StringIO

from app.parsers.specification.lexer import SpecificationLexer
from app.parsers.specification.token_types import TokenType
from app.parsers.specification.tokens import Token


def assert_token(
    token: Token,
    *,
    token_type: TokenType,
    value: str,
    line: int,
    column: int,
    source_file: str = "",
    section: str = "",
) -> None:
    """
    Assert every externally visible token attribute.
    """

    assert token.type is token_type
    assert token.value == value
    assert token.line == line
    assert token.column == column
    assert token.source_file == source_file
    assert token.section == section


def test_complete_structural_token_stream() -> None:
    text = (
        "Module Name: mux2to1\n"
        "Inputs:\n"
        "a\n"
        "Detailed behavior text.\n"
    )

    tokens = SpecificationLexer(
        text,
        source_file="specification.txt",
    ).tokenize()

    expected_types = [
        TokenType.KEY,
        TokenType.COLON,
        TokenType.VALUE,
        TokenType.NEWLINE,
        TokenType.SECTION_HEADER,
        TokenType.NEWLINE,
        TokenType.LIST_ITEM,
        TokenType.NEWLINE,
        TokenType.TEXT,
        TokenType.NEWLINE,
        TokenType.EOF,
    ]

    assert [token.type for token in tokens] == expected_types

    assert_token(
        tokens[0],
        token_type=TokenType.KEY,
        value="Module Name",
        line=1,
        column=1,
        source_file="specification.txt",
    )
    assert_token(
        tokens[1],
        token_type=TokenType.COLON,
        value=":",
        line=1,
        column=12,
        source_file="specification.txt",
    )
    assert_token(
        tokens[2],
        token_type=TokenType.VALUE,
        value="mux2to1",
        line=1,
        column=14,
        source_file="specification.txt",
    )
    assert_token(
        tokens[4],
        token_type=TokenType.SECTION_HEADER,
        value="Inputs",
        line=2,
        column=1,
        source_file="specification.txt",
        section="Inputs",
    )
    assert_token(
        tokens[6],
        token_type=TokenType.LIST_ITEM,
        value="a",
        line=3,
        column=1,
        source_file="specification.txt",
        section="Inputs",
    )
    assert_token(
        tokens[8],
        token_type=TokenType.TEXT,
        value="Detailed behavior text.",
        line=4,
        column=1,
        source_file="specification.txt",
        section="Inputs",
    )
    assert_token(
        tokens[-1],
        token_type=TokenType.EOF,
        value="",
        line=5,
        column=1,
        source_file="specification.txt",
        section="Inputs",
    )


def test_indented_key_value_locations() -> None:
    text = "  Module Name:   mux2to1\n"

    tokens = SpecificationLexer(text).tokenize()

    assert_token(
        tokens[0],
        token_type=TokenType.KEY,
        value="Module Name",
        line=1,
        column=3,
    )
    assert_token(
        tokens[1],
        token_type=TokenType.COLON,
        value=":",
        line=1,
        column=14,
    )
    assert_token(
        tokens[2],
        token_type=TokenType.VALUE,
        value="mux2to1",
        line=1,
        column=18,
    )
    assert_token(
        tokens[3],
        token_type=TokenType.NEWLINE,
        value="\n",
        line=1,
        column=25,
    )


def test_section_context_changes_deterministically() -> None:
    text = (
        "Project Name: RIVA\n"
        "Inputs:\n"
        "clk\n"
        "Outputs:\n"
        "result\n"
    )

    tokens = SpecificationLexer(text).tokenize()

    key_token = tokens[0]
    input_header = tokens[4]
    input_item = tokens[6]
    output_header = tokens[8]
    output_item = tokens[10]
    eof_token = tokens[-1]

    assert key_token.section == ""
    assert input_header.section == "Inputs"
    assert input_item.section == "Inputs"
    assert output_header.section == "Outputs"
    assert output_item.section == "Outputs"
    assert eof_token.section == "Outputs"


def test_blank_lines_emit_newline_tokens() -> None:
    tokens = SpecificationLexer("\n \t\n").tokenize()

    assert [token.type for token in tokens] == [
        TokenType.NEWLINE,
        TokenType.NEWLINE,
        TokenType.EOF,
    ]

    assert_token(
        tokens[0],
        token_type=TokenType.NEWLINE,
        value="\n",
        line=1,
        column=1,
    )
    assert_token(
        tokens[1],
        token_type=TokenType.NEWLINE,
        value="\n",
        line=2,
        column=3,
    )
    assert_token(
        tokens[2],
        token_type=TokenType.EOF,
        value="",
        line=3,
        column=1,
    )


def test_crlf_input_preserves_line_tracking() -> None:
    tokens = SpecificationLexer("Inputs:\r\nclk\r\n").tokenize()

    assert [token.type for token in tokens] == [
        TokenType.SECTION_HEADER,
        TokenType.NEWLINE,
        TokenType.LIST_ITEM,
        TokenType.NEWLINE,
        TokenType.EOF,
    ]

    assert_token(
        tokens[1],
        token_type=TokenType.NEWLINE,
        value="\n",
        line=1,
        column=9,
        section="Inputs",
    )
    assert_token(
        tokens[2],
        token_type=TokenType.LIST_ITEM,
        value="clk",
        line=2,
        column=1,
        section="Inputs",
    )
    assert_token(
        tokens[3],
        token_type=TokenType.NEWLINE,
        value="\n",
        line=2,
        column=5,
        section="Inputs",
    )
    assert_token(
        tokens[4],
        token_type=TokenType.EOF,
        value="",
        line=3,
        column=1,
        section="Inputs",
    )


def test_final_line_without_physical_newline() -> None:
    tokens = SpecificationLexer("Outputs:\ny").tokenize()

    assert [token.type for token in tokens] == [
        TokenType.SECTION_HEADER,
        TokenType.NEWLINE,
        TokenType.LIST_ITEM,
        TokenType.NEWLINE,
        TokenType.EOF,
    ]

    assert_token(
        tokens[3],
        token_type=TokenType.NEWLINE,
        value="\n",
        line=2,
        column=2,
        section="Outputs",
    )
    assert_token(
        tokens[4],
        token_type=TokenType.EOF,
        value="",
        line=2,
        column=2,
        section="Outputs",
    )


def test_value_preserves_additional_colons() -> None:
    tokens = SpecificationLexer(
        "Reference: https://example.com/path:a\n"
    ).tokenize()

    assert tokens[0].value == "Reference"
    assert tokens[1].type is TokenType.COLON
    assert tokens[2].type is TokenType.VALUE
    assert tokens[2].value == "https://example.com/path:a"


def test_empty_document_contains_only_eof() -> None:
    tokens = SpecificationLexer("").tokenize()

    assert len(tokens) == 1

    assert_token(
        tokens[0],
        token_type=TokenType.EOF,
        value="",
        line=1,
        column=1,
    )


def test_tokenize_is_repeatable() -> None:
    lexer = SpecificationLexer(
        "Inputs:\nclk\n",
        source_file="repeatable.txt",
    )

    first_tokens = lexer.tokenize()
    second_tokens = lexer.tokenize()

    assert first_tokens == second_tokens
    assert first_tokens is not second_tokens


def test_tokenize_has_no_debug_output() -> None:
    output = StringIO()

    with redirect_stdout(output):
        SpecificationLexer("Inputs:\nclk\n").tokenize()

    assert output.getvalue() == ""


def test_invalid_constructor_arguments_are_rejected() -> None:
    try:
        SpecificationLexer(123)  # type: ignore[arg-type]

    except TypeError as error:
        assert str(error) == "text must be a string."

    else:
        raise AssertionError(
            "Expected TypeError for a non-string text argument."
        )

    try:
        SpecificationLexer(
            "Inputs:\n",
            source_file=123,  # type: ignore[arg-type]
        )

    except TypeError as error:
        assert str(error) == "source_file must be a string."

    else:
        raise AssertionError(
            "Expected TypeError for a non-string source filename."
        )


def main() -> None:
    tests = (
        test_complete_structural_token_stream,
        test_indented_key_value_locations,
        test_section_context_changes_deterministically,
        test_blank_lines_emit_newline_tokens,
        test_crlf_input_preserves_line_tracking,
        test_final_line_without_physical_newline,
        test_value_preserves_additional_colons,
        test_empty_document_contains_only_eof,
        test_tokenize_is_repeatable,
        test_tokenize_has_no_debug_output,
        test_invalid_constructor_arguments_are_rejected,
    )

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print("\nSpecificationLexer tests passed.")


if __name__ == "__main__":
    main()
