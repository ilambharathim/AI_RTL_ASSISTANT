"""
RIVA specification document lexer.

Converts normalized specification text into generic document tokens using
the shared scanner, line reader, classifier, and token builder.

The lexer recognizes document structure only. Engineering meaning belongs
to the parser and semantic-analysis stages.
"""

from app.parsers.specification.classifier import (
    DocumentClassifier,
    LineType,
)
from app.parsers.specification.line_reader import LineReader
from app.parsers.specification.scanner import Scanner
from app.parsers.specification.token_builder import TokenBuilder
from app.parsers.specification.token_types import TokenType
from app.parsers.specification.tokens import Token


class SpecificationLexer:
    """
    Deterministic lexer for normalized specification documents.

    The lexer emits generic structural tokens while preserving source
    locations and section context. Calling ``tokenize`` multiple times
    returns a fresh token stream each time.
    """

    def __init__(self, text: str, source_file: str = "") -> None:
        if not isinstance(text, str):
            raise TypeError("text must be a string.")

        if not isinstance(source_file, str):
            raise TypeError("source_file must be a string.")

        self._text = text
        self._source_file = source_file

    def tokenize(self) -> list[Token]:
        """
        Convert the complete document into a token stream.

        Every logical input line produces a NEWLINE token. The stream always
        ends with exactly one EOF token.
        """

        scanner = Scanner(self._text)
        line_reader = LineReader(scanner)

        tokens: list[Token] = []
        current_section = ""

        while not line_reader.eof():
            line_start = scanner.position()
            line_start_index = line_start.index

            raw_line = line_reader.next_line()

            if raw_line is None:
                break

            line_tokens, current_section = self._tokenize_line(
                raw_line=raw_line,
                line_number=line_start.line,
                current_section=current_section,
            )

            tokens.extend(line_tokens)

            newline_column = self._newline_column(
                scanner=scanner,
                line_start_index=line_start_index,
                line_start_number=line_start.line,
            )

            tokens.append(
                self._build_token(
                    token_type=TokenType.NEWLINE,
                    value="\n",
                    line=line_start.line,
                    column=newline_column,
                    section=current_section,
                )
            )

        eof_position = scanner.position()

        tokens.append(
            self._build_token(
                token_type=TokenType.EOF,
                value="",
                line=eof_position.line,
                column=eof_position.column,
                section=current_section,
            )
        )

        return tokens

    def _tokenize_line(
        self,
        raw_line: str,
        line_number: int,
        current_section: str,
    ) -> tuple[list[Token], str]:
        """
        Tokenize one logical line and return its resulting section context.
        """

        line_type = DocumentClassifier.classify(raw_line)
        stripped_line = raw_line.strip()

        if line_type is LineType.EMPTY:
            return [], current_section

        if line_type is LineType.SECTION_HEADER:
            section_name = stripped_line[:-1].strip()
            column = self._first_content_column(raw_line)

            return (
                [
                    self._build_token(
                        token_type=TokenType.SECTION_HEADER,
                        value=section_name,
                        line=line_number,
                        column=column,
                        section=section_name,
                    )
                ],
                section_name,
            )

        if line_type is LineType.KEY_VALUE:
            return (
                self._tokenize_key_value(
                    raw_line=raw_line,
                    line_number=line_number,
                    section=current_section,
                ),
                current_section,
            )

        token_type = (
            TokenType.LIST_ITEM
            if line_type is LineType.LIST_ITEM
            else TokenType.TEXT
        )

        return (
            [
                self._build_token(
                    token_type=token_type,
                    value=stripped_line,
                    line=line_number,
                    column=self._first_content_column(raw_line),
                    section=current_section,
                )
            ],
            current_section,
        )

    def _tokenize_key_value(
        self,
        raw_line: str,
        line_number: int,
        section: str,
    ) -> list[Token]:
        """
        Tokenize a generic ``key: value`` line.
        """

        colon_index = raw_line.index(":")
        key = raw_line[:colon_index].strip()

        value_start_index = colon_index + 1

        while (
            value_start_index < len(raw_line)
            and raw_line[value_start_index].isspace()
        ):
            value_start_index += 1

        value = raw_line[value_start_index:].strip()

        tokens = [
            self._build_token(
                token_type=TokenType.KEY,
                value=key,
                line=line_number,
                column=self._first_content_column(raw_line),
                section=section,
            ),
            self._build_token(
                token_type=TokenType.COLON,
                value=":",
                line=line_number,
                column=colon_index + 1,
                section=section,
            ),
        ]

        if value:
            tokens.append(
                self._build_token(
                    token_type=TokenType.VALUE,
                    value=value,
                    line=line_number,
                    column=value_start_index + 1,
                    section=section,
                )
            )

        return tokens

    def _build_token(
        self,
        token_type: TokenType,
        value: str,
        line: int,
        column: int,
        section: str,
    ) -> Token:
        """
        Build a validated token using the shared TokenBuilder.
        """

        return TokenBuilder.build(
            token_type=token_type,
            value=value,
            line=line,
            column=column,
            source_file=self._source_file,
            section=section,
        )

    @staticmethod
    def _first_content_column(line: str) -> int:
        """
        Return the one-based column of the first non-whitespace character.
        """

        for index, character in enumerate(line):
            if not character.isspace():
                return index + 1

        return 1

    @staticmethod
    def _newline_column(
        scanner: Scanner,
        line_start_index: int,
        line_start_number: int,
    ) -> int:
        """
        Return the physical or synthetic newline column.

        When the source contains a newline, the scanner index delta preserves
        correct metadata for both LF and CRLF input. For a final line without
        a newline, the token is placed immediately after its final character.
        """

        if scanner.line > line_start_number:
            return scanner.index - line_start_index

        return scanner.column
