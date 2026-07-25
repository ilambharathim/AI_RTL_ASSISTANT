"""
Regression tests for recoverable specification parsing.
"""

from contextlib import redirect_stderr, redirect_stdout
from io import StringIO

from app.domain.ast.keyvalue_node import KeyValueNode
from app.domain.ast.listitem_node import ListItemNode
from app.domain.ast.text_node import TextNode
from app.engines.diagnostics.diagnostic_severity import DiagnosticSeverity
from app.parsers.specification.exceptions import SpecificationSyntaxError
from app.parsers.specification.parser import SpecificationParser
from app.parsers.specification.parser_diagnostic_code import (
    SpecificationParserDiagnosticCode,
)
from app.parsers.specification.token_types import TokenType
from app.parsers.specification.tokens import Token


SOURCE_FILE = "broken.txt"


def make_token(
    token_type: TokenType,
    value: str,
    *,
    line: int,
    column: int = 1,
    source_file: str = SOURCE_FILE,
) -> Token:
    return Token(
        type=token_type,
        value=value,
        line=line,
        column=column,
        source_file=source_file,
    )


def test_valid_stream_matches_strict_parse() -> None:
    tokens = (
        make_token(
            TokenType.KEY,
            "Project Title",
            line=1,
        ),
        make_token(
            TokenType.COLON,
            ":",
            line=1,
            column=14,
        ),
        make_token(
            TokenType.VALUE,
            "RIVA",
            line=1,
            column=16,
        ),
        make_token(
            TokenType.NEWLINE,
            "\n",
            line=1,
            column=20,
        ),
        make_token(
            TokenType.SECTION_HEADER,
            "Inputs",
            line=2,
        ),
        make_token(
            TokenType.NEWLINE,
            "\n",
            line=2,
            column=8,
        ),
        make_token(
            TokenType.LIST_ITEM,
            "a",
            line=3,
        ),
        make_token(
            TokenType.NEWLINE,
            "\n",
            line=3,
            column=2,
        ),
        make_token(
            TokenType.EOF,
            "",
            line=4,
        ),
    )

    strict_document = SpecificationParser(tokens).parse()
    result = SpecificationParser(tokens).parse_with_diagnostics()

    assert result.is_successful
    assert not result.has_errors
    assert result.diagnostic_count == 0
    assert result.diagnostics == ()
    assert result.document == strict_document
    assert result.document is not strict_document

    assert len(result.document.entries) == 1
    assert isinstance(result.document.entries[0], KeyValueNode)
    assert result.document.entries[0].key == "Project Title"
    assert result.document.entries[0].value == "RIVA"

    assert len(result.document.sections) == 1
    assert result.document.sections[0].name == "Inputs"
    assert len(result.document.sections[0].entries) == 1
    assert isinstance(
        result.document.sections[0].entries[0],
        ListItemNode,
    )
    assert result.document.sections[0].entries[0].value == "a"


def test_multiple_errors_are_aggregated_in_order() -> None:
    tokens = (
        make_token(
            TokenType.TEXT,
            "Preamble",
            line=1,
        ),
        make_token(
            TokenType.NEWLINE,
            "\n",
            line=1,
            column=9,
        ),
        make_token(
            TokenType.IDENTIFIER,
            "invalid",
            line=2,
        ),
        make_token(
            TokenType.NEWLINE,
            "\n",
            line=2,
            column=8,
        ),
        make_token(
            TokenType.KEY,
            "Module Name",
            line=3,
        ),
        make_token(
            TokenType.VALUE,
            "mux2to1",
            line=3,
            column=13,
        ),
        make_token(
            TokenType.NEWLINE,
            "\n",
            line=3,
            column=20,
        ),
        make_token(
            TokenType.SECTION_HEADER,
            "Inputs",
            line=4,
        ),
        make_token(
            TokenType.NEWLINE,
            "\n",
            line=4,
            column=8,
        ),
        make_token(
            TokenType.LIST_ITEM,
            "a",
            line=5,
        ),
        make_token(
            TokenType.NEWLINE,
            "\n",
            line=5,
            column=2,
        ),
        make_token(
            TokenType.TEXT,
            "   ",
            line=6,
        ),
        make_token(
            TokenType.NEWLINE,
            "\n",
            line=6,
            column=4,
        ),
        make_token(
            TokenType.LIST_ITEM,
            "b",
            line=7,
        ),
        make_token(
            TokenType.NEWLINE,
            "\n",
            line=7,
            column=2,
        ),
        make_token(
            TokenType.EOF,
            "",
            line=8,
        ),
    )

    result = SpecificationParser(tokens).parse_with_diagnostics()

    assert not result.is_successful
    assert result.has_errors
    assert result.diagnostic_count == 3
    assert result.error_count == 3
    assert result.warning_count == 0
    assert result.info_count == 0

    assert tuple(
        diagnostic.code
        for diagnostic in result.diagnostics
    ) == (
        SpecificationParserDiagnosticCode.UNEXPECTED_TOKEN.value,
        (
            SpecificationParserDiagnosticCode
            .EXPECTED_COLON_AFTER_KEY
            .value
        ),
        SpecificationParserDiagnosticCode.EMPTY_TEXT.value,
    )

    assert tuple(
        diagnostic.message
        for diagnostic in result.diagnostics
    ) == (
        "Unexpected IDENTIFIER token.",
        "Expected COLON after key.",
        "Text must not be empty.",
    )

    assert tuple(
        (diagnostic.line, diagnostic.column)
        for diagnostic in result.diagnostics
    ) == (
        (2, 1),
        (3, 13),
        (6, 1),
    )

    assert len(result.document.entries) == 1
    assert isinstance(result.document.entries[0], TextNode)
    assert result.document.entries[0].value == "Preamble"

    assert len(result.document.sections) == 1
    section = result.document.sections[0]

    assert section.name == "Inputs"
    assert tuple(
        entry.value
        for entry in section.entries
    ) == ("a", "b")


def test_diagnostics_preserve_complete_source_contract() -> None:
    tokens = (
        make_token(
            TokenType.KEY,
            "Module Name",
            line=4,
            column=3,
            source_file="design-spec.txt",
        ),
        make_token(
            TokenType.VALUE,
            "mux2to1",
            line=4,
            column=15,
            source_file="design-spec.txt",
        ),
        make_token(
            TokenType.NEWLINE,
            "\n",
            line=4,
            column=22,
            source_file="design-spec.txt",
        ),
        make_token(
            TokenType.EOF,
            "",
            line=5,
            source_file="design-spec.txt",
        ),
    )

    result = SpecificationParser(tokens).parse_with_diagnostics()

    assert result.diagnostic_count == 1

    diagnostic = result.diagnostics[0]

    assert diagnostic.code == "SPEC-PARSE-007"
    assert diagnostic.message == "Expected COLON after key."
    assert diagnostic.severity is DiagnosticSeverity.ERROR
    assert diagnostic.stage == "specification-parser"
    assert diagnostic.line == 4
    assert diagnostic.column == 15
    assert diagnostic.source_file == "design-spec.txt"

    assert str(diagnostic) == (
        "design-spec.txt:4:15: ERROR SPEC-PARSE-007 "
        "[specification-parser]: Expected COLON after key."
    )


def test_malformed_section_does_not_become_active() -> None:
    tokens = (
        make_token(
            TokenType.SECTION_HEADER,
            "Inputs",
            line=1,
        ),
        make_token(
            TokenType.NEWLINE,
            "\n",
            line=1,
            column=8,
        ),
        make_token(
            TokenType.LIST_ITEM,
            "a",
            line=2,
        ),
        make_token(
            TokenType.NEWLINE,
            "\n",
            line=2,
            column=2,
        ),
        make_token(
            TokenType.SECTION_HEADER,
            "   ",
            line=3,
        ),
        make_token(
            TokenType.NEWLINE,
            "\n",
            line=3,
            column=4,
        ),
        make_token(
            TokenType.LIST_ITEM,
            "b",
            line=4,
        ),
        make_token(
            TokenType.NEWLINE,
            "\n",
            line=4,
            column=2,
        ),
        make_token(
            TokenType.SECTION_HEADER,
            "Outputs",
            line=5,
        ),
        make_token(
            TokenType.NEWLINE,
            "\n",
            line=5,
            column=9,
        ),
        make_token(
            TokenType.LIST_ITEM,
            "y",
            line=6,
        ),
        make_token(
            TokenType.NEWLINE,
            "\n",
            line=6,
            column=2,
        ),
        make_token(
            TokenType.EOF,
            "",
            line=7,
        ),
    )

    result = SpecificationParser(tokens).parse_with_diagnostics()

    assert result.diagnostic_count == 1
    assert result.diagnostics[0].code == (
        SpecificationParserDiagnosticCode.EMPTY_SECTION_HEADER.value
    )

    assert tuple(
        section.name
        for section in result.document.sections
    ) == ("Inputs", "Outputs")

    inputs, outputs = result.document.sections

    assert tuple(
        entry.value
        for entry in inputs.entries
    ) == ("a", "b")

    assert tuple(
        entry.value
        for entry in outputs.entries
    ) == ("y",)


def test_missing_newline_preserves_later_source_line() -> None:
    tokens = (
        make_token(
            TokenType.TEXT,
            "Discarded text",
            line=1,
        ),
        make_token(
            TokenType.TEXT,
            "Recovered text",
            line=2,
        ),
        make_token(
            TokenType.NEWLINE,
            "\n",
            line=2,
            column=15,
        ),
        make_token(
            TokenType.EOF,
            "",
            line=3,
        ),
    )

    result = SpecificationParser(tokens).parse_with_diagnostics()

    assert result.diagnostic_count == 1

    diagnostic = result.diagnostics[0]

    assert diagnostic.code == (
        SpecificationParserDiagnosticCode
        .EXPECTED_NEWLINE_AFTER_TEXT
        .value
    )
    assert diagnostic.line == 2
    assert diagnostic.column == 1

    assert len(result.document.entries) == 1
    assert isinstance(result.document.entries[0], TextNode)
    assert result.document.entries[0].value == "Recovered text"


def test_recovery_at_eof_returns_valid_partial_document() -> None:
    tokens = (
        make_token(
            TokenType.LIST_ITEM,
            "clk",
            line=1,
        ),
        make_token(
            TokenType.EOF,
            "",
            line=2,
        ),
    )

    result = SpecificationParser(tokens).parse_with_diagnostics()

    assert result.diagnostic_count == 1
    assert result.diagnostics[0].code == (
        SpecificationParserDiagnosticCode
        .EXPECTED_NEWLINE_AFTER_LIST_ITEM
        .value
    )
    assert result.diagnostics[0].line == 2
    assert result.document.entries == []
    assert result.document.sections == []


def test_synchronization_discards_failed_line_and_progresses() -> None:
    tokens = (
        make_token(
            TokenType.IDENTIFIER,
            "invalid",
            line=1,
        ),
        make_token(
            TokenType.NUMBER,
            "123",
            line=1,
            column=9,
        ),
        make_token(
            TokenType.COMMA,
            ",",
            line=1,
            column=12,
        ),
        make_token(
            TokenType.NEWLINE,
            "\n",
            line=1,
            column=13,
        ),
        make_token(
            TokenType.TEXT,
            "Valid later text",
            line=2,
        ),
        make_token(
            TokenType.NEWLINE,
            "\n",
            line=2,
            column=17,
        ),
        make_token(
            TokenType.EOF,
            "",
            line=3,
        ),
    )

    result = SpecificationParser(tokens).parse_with_diagnostics()

    assert result.diagnostic_count == 1
    assert result.diagnostics[0].code == (
        SpecificationParserDiagnosticCode.UNEXPECTED_TOKEN.value
    )

    assert len(result.document.entries) == 1
    assert result.document.entries[0].value == "Valid later text"


def test_recovery_is_repeatable_independent_and_silent() -> None:
    tokens = (
        make_token(
            TokenType.SECTION_HEADER,
            "Inputs",
            line=1,
        ),
        make_token(
            TokenType.NEWLINE,
            "\n",
            line=1,
            column=8,
        ),
        make_token(
            TokenType.TEXT,
            "   ",
            line=2,
        ),
        make_token(
            TokenType.NEWLINE,
            "\n",
            line=2,
            column=4,
        ),
        make_token(
            TokenType.LIST_ITEM,
            "a",
            line=3,
        ),
        make_token(
            TokenType.NEWLINE,
            "\n",
            line=3,
            column=2,
        ),
        make_token(
            TokenType.EOF,
            "",
            line=4,
        ),
    )

    parser = SpecificationParser(tokens)
    stdout = StringIO()
    stderr = StringIO()

    with redirect_stdout(stdout), redirect_stderr(stderr):
        first = parser.parse_with_diagnostics()
        second = parser.parse_with_diagnostics()

    assert stdout.getvalue() == ""
    assert stderr.getvalue() == ""

    assert first == second
    assert first is not second
    assert first.document is not second.document
    assert first.diagnostics is not second.diagnostics

    assert (
        first.document.sections[0]
        is not second.document.sections[0]
    )
    assert (
        first.document.sections[0].entries[0]
        is not second.document.sections[0].entries[0]
    )


def test_strict_parse_remains_fail_fast() -> None:
    tokens = (
        make_token(
            TokenType.IDENTIFIER,
            "invalid",
            line=1,
        ),
        make_token(
            TokenType.NEWLINE,
            "\n",
            line=1,
            column=8,
        ),
        make_token(
            TokenType.TEXT,
            "Valid later text",
            line=2,
        ),
        make_token(
            TokenType.NEWLINE,
            "\n",
            line=2,
            column=17,
        ),
        make_token(
            TokenType.EOF,
            "",
            line=3,
        ),
    )

    parser = SpecificationParser(tokens)

    try:
        parser.parse()
    except SpecificationSyntaxError as error:
        assert error.code == (
            SpecificationParserDiagnosticCode.UNEXPECTED_TOKEN.value
        )
        assert error.line == 1
        assert error.column == 1
    else:
        raise AssertionError(
            "Strict parse() must stop at the first syntax error."
        )

    result = parser.parse_with_diagnostics()

    assert result.diagnostic_count == 1
    assert result.document.entries[0].value == "Valid later text"


def main() -> None:
    tests = (
        test_valid_stream_matches_strict_parse,
        test_multiple_errors_are_aggregated_in_order,
        test_diagnostics_preserve_complete_source_contract,
        test_malformed_section_does_not_become_active,
        test_missing_newline_preserves_later_source_line,
        test_recovery_at_eof_returns_valid_partial_document,
        test_synchronization_discards_failed_line_and_progresses,
        test_recovery_is_repeatable_independent_and_silent,
        test_strict_parse_remains_fail_fast,
    )

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print("\nSpecificationParser recovery tests passed.")


if __name__ == "__main__":
    main()
