"""
Regression tests for the RIVA generic specification parser.
"""

from contextlib import redirect_stdout
from io import StringIO

from app.domain.ast.document_node import DocumentNode
from app.domain.ast.keyvalue_node import KeyValueNode
from app.domain.ast.listitem_node import ListItemNode
from app.domain.ast.section_node import SectionNode
from app.domain.ast.text_node import TextNode
from app.parsers.specification.exceptions import (
    SpecificationSyntaxError,
    SpecificationTokenStreamError,
)
from app.parsers.specification.lexer import SpecificationLexer
from app.parsers.specification.parser import SpecificationParser
from app.parsers.specification.token_types import TokenType
from app.parsers.specification.tokens import Token


def make_token(
    token_type: TokenType,
    value: str,
    *,
    line: int = 1,
    column: int = 1,
    source_file: str = "",
    section: str = "",
) -> Token:
    return Token(
        type=token_type,
        value=value,
        line=line,
        column=column,
        source_file=source_file,
        section=section,
    )


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


def test_complete_document_is_parsed() -> None:
    text = (
        "Project Name: RIVA\n"
        "Description:\n"
        "\n"
        "Inputs:\n"
        "clk\n"
        "rst_n\n"
        "\n"
        "Behavior:\n"
        "The output shall update combinationally.\n"
    )

    tokens = SpecificationLexer(
        text,
        source_file="mux_spec.txt",
    ).tokenize()

    document = SpecificationParser(tokens).parse()

    assert isinstance(document, DocumentNode)
    assert document.title == ""
    assert document.line == 1
    assert document.column == 1
    assert document.source_file == "mux_spec.txt"

    assert len(document.entries) == 1
    assert len(document.sections) == 3
    assert document.child_count() == 4

    project_name = document.entries[0]

    assert isinstance(project_name, KeyValueNode)
    assert project_name.key == "Project Name"
    assert project_name.value == "RIVA"
    assert project_name.line == 1
    assert project_name.column == 1
    assert project_name.source_file == "mux_spec.txt"

    description = document.sections[0]
    inputs = document.sections[1]
    behavior = document.sections[2]

    assert isinstance(description, SectionNode)
    assert description.name == "Description"
    assert description.line == 2
    assert description.entries == []

    assert isinstance(inputs, SectionNode)
    assert inputs.name == "Inputs"
    assert inputs.line == 4
    assert inputs.column == 1
    assert inputs.source_file == "mux_spec.txt"

    assert [entry.value for entry in inputs.entries] == ["clk", "rst_n"]
    assert all(isinstance(entry, ListItemNode) for entry in inputs.entries)
    assert [entry.line for entry in inputs.entries] == [5, 6]

    assert isinstance(behavior, SectionNode)
    assert behavior.name == "Behavior"
    assert behavior.line == 8
    assert len(behavior.entries) == 1

    behavior_text = behavior.entries[0]

    assert isinstance(behavior_text, TextNode)
    assert behavior_text.value == (
        "The output shall update combinationally."
    )
    assert behavior_text.line == 9


def test_empty_document_is_parsed() -> None:
    tokens = SpecificationLexer(
        "",
        source_file="empty.txt",
    ).tokenize()

    document = SpecificationParser(tokens).parse()

    assert document.entries == []
    assert document.sections == []
    assert document.children == []
    assert document.line == 1
    assert document.column == 1
    assert document.source_file == "empty.txt"


def test_entries_follow_active_section() -> None:
    text = (
        "Document Key: document value\n"
        "First:\n"
        "a\n"
        "First text entry.\n"
        "Second:\n"
        "Second Key: second value\n"
    )

    document = SpecificationParser(
        SpecificationLexer(text).tokenize()
    ).parse()

    assert len(document.entries) == 1
    assert document.entries[0].key == "Document Key"

    assert len(document.sections) == 2
    assert [section.name for section in document.sections] == [
        "First",
        "Second",
    ]

    first = document.sections[0]
    second = document.sections[1]

    assert isinstance(first.entries[0], ListItemNode)
    assert isinstance(first.entries[1], TextNode)

    assert len(second.entries) == 1
    assert isinstance(second.entries[0], KeyValueNode)
    assert second.entries[0].key == "Second Key"
    assert second.entries[0].value == "second value"


def test_parse_is_repeatable_and_independent() -> None:
    parser = SpecificationParser(
        SpecificationLexer(
            "Inputs:\nclk\n",
            source_file="repeatable.txt",
        ).tokenize()
    )

    first_document = parser.parse()
    second_document = parser.parse()

    assert first_document == second_document
    assert first_document is not second_document
    assert first_document.sections is not second_document.sections
    assert first_document.sections[0] is not second_document.sections[0]
    assert (
        first_document.sections[0].entries[0]
        is not second_document.sections[0].entries[0]
    )


def test_parse_has_no_debug_output() -> None:
    parser = SpecificationParser(
        SpecificationLexer("Inputs:\nclk\n").tokenize()
    )
    output = StringIO()

    with redirect_stdout(output):
        parser.parse()

    assert output.getvalue() == ""


def test_constructor_rejects_invalid_token_container() -> None:
    assert_raises(
        TypeError,
        "tokens must be a sequence of Token objects.",
        lambda: SpecificationParser("invalid"),
    )
    assert_raises(
        TypeError,
        "tokens must be a sequence of Token objects.",
        lambda: SpecificationParser(123),
    )


def test_token_stream_requires_tokens_and_one_final_eof() -> None:
    assert_raises(
        SpecificationTokenStreamError,
        "Token stream must contain at least one token.",
        lambda: SpecificationParser([]),
    )

    assert_raises(
        SpecificationTokenStreamError,
        "Token stream must contain exactly one EOF token.",
        lambda: SpecificationParser(
            [
                make_token(TokenType.TEXT, "text"),
                make_token(TokenType.NEWLINE, "\n", column=5),
            ]
        ),
    )

    assert_raises(
        SpecificationTokenStreamError,
        "Token stream must contain exactly one EOF token.",
        lambda: SpecificationParser(
            [
                make_token(TokenType.EOF, ""),
                make_token(TokenType.EOF, "", column=2),
            ]
        ),
    )

    assert_raises(
        SpecificationTokenStreamError,
        "EOF token must be the final token in the stream.",
        lambda: SpecificationParser(
            [
                make_token(TokenType.EOF, ""),
                make_token(TokenType.NEWLINE, "\n", column=2),
            ]
        ),
    )


def test_token_stream_rejects_invalid_members() -> None:
    assert_raises(
        SpecificationTokenStreamError,
        "tokens[0] must be a Token.",
        lambda: SpecificationParser(["invalid"]),
    )

    invalid_source_token = make_token(TokenType.EOF, "")
    invalid_source_token.source_file = None

    assert_raises(
        SpecificationTokenStreamError,
        "tokens[0].source_file must be a string.",
        lambda: SpecificationParser([invalid_source_token]),
    )

    invalid_section_token = make_token(TokenType.EOF, "")
    invalid_section_token.section = None

    assert_raises(
        SpecificationTokenStreamError,
        "tokens[0].section must be a string.",
        lambda: SpecificationParser([invalid_section_token]),
    )

    invalid_line_token = make_token(TokenType.EOF, "")
    invalid_line_token.line = 0

    assert_raises(
        SpecificationTokenStreamError,
        (
            "tokens[0].line must be an integer "
            "greater than or equal to 1."
        ),
        lambda: SpecificationParser([invalid_line_token]),
    )

    invalid_column_token = make_token(TokenType.EOF, "")
    invalid_column_token.column = 0

    assert_raises(
        SpecificationTokenStreamError,
        (
            "tokens[0].column must be an integer "
            "greater than or equal to 1."
        ),
        lambda: SpecificationParser([invalid_column_token]),
    )


def test_missing_colon_reports_source_location() -> None:
    tokens = [
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
    ]

    error = assert_raises(
        SpecificationSyntaxError,
        "broken.txt:1:13: Expected COLON after key.",
        lambda: SpecificationParser(tokens).parse(),
    )

    assert isinstance(error, SpecificationSyntaxError)
    assert error.message == "Expected COLON after key."
    assert error.line == 1
    assert error.column == 13
    assert error.source_file == "broken.txt"


def test_missing_newline_is_rejected() -> None:
    tokens = [
        make_token(TokenType.TEXT, "text"),
        make_token(TokenType.EOF, "", column=5),
    ]

    assert_raises(
        SpecificationSyntaxError,
        "<memory>:1:5: Expected NEWLINE after text.",
        lambda: SpecificationParser(tokens).parse(),
    )


def test_unexpected_reserved_token_is_rejected() -> None:
    tokens = [
        make_token(TokenType.IDENTIFIER, "clk"),
        make_token(TokenType.NEWLINE, "\n", column=4),
        make_token(TokenType.EOF, "", line=2),
    ]

    assert_raises(
        SpecificationSyntaxError,
        "<memory>:1:1: Unexpected IDENTIFIER token.",
        lambda: SpecificationParser(tokens).parse(),
    )


def test_empty_structural_values_are_rejected() -> None:
    empty_section_tokens = [
        make_token(TokenType.SECTION_HEADER, ""),
        make_token(TokenType.NEWLINE, "\n"),
        make_token(TokenType.EOF, "", line=2),
    ]

    assert_raises(
        SpecificationSyntaxError,
        "<memory>:1:1: Section header must not be empty.",
        lambda: SpecificationParser(empty_section_tokens).parse(),
    )

    empty_value_tokens = [
        make_token(TokenType.KEY, "Description"),
        make_token(TokenType.COLON, ":", column=12),
        make_token(TokenType.VALUE, "   ", column=14),
        make_token(TokenType.NEWLINE, "\n", column=17),
        make_token(TokenType.EOF, "", line=2),
    ]

    assert_raises(
        SpecificationSyntaxError,
        "<memory>:1:14: VALUE token must not be empty.",
        lambda: SpecificationParser(empty_value_tokens).parse(),
    )


def main() -> None:
    tests = (
        test_complete_document_is_parsed,
        test_empty_document_is_parsed,
        test_entries_follow_active_section,
        test_parse_is_repeatable_and_independent,
        test_parse_has_no_debug_output,
        test_constructor_rejects_invalid_token_container,
        test_token_stream_requires_tokens_and_one_final_eof,
        test_token_stream_rejects_invalid_members,
        test_missing_colon_reports_source_location,
        test_missing_newline_is_rejected,
        test_unexpected_reserved_token_is_rejected,
        test_empty_structural_values_are_rejected,
    )

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print("\nSpecificationParser tests passed.")


if __name__ == "__main__":
    main()
