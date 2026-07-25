"""
Deterministic parser for the RIVA generic specification AST.

The parser consumes generic lexer tokens and constructs document, section,
key-value, list-item, and free-form text nodes. Engineering interpretation
belongs to later semantic-analysis stages.
"""

from __future__ import annotations

from collections.abc import Sequence

from app.domain.ast.ast_node import ASTNode
from app.domain.ast.document_node import DocumentNode
from app.domain.ast.keyvalue_node import KeyValueNode
from app.domain.ast.listitem_node import ListItemNode
from app.domain.ast.section_node import SectionNode
from app.domain.ast.text_node import TextNode
from app.parsers.specification.exceptions import (
    SpecificationSyntaxError,
    SpecificationTokenStreamError,
)
from app.parsers.specification.token_types import TokenType
from app.parsers.specification.tokens import Token


class SpecificationParser:
    """
    Parse a validated generic specification token stream.

    Supported grammar:

    document
        := (NEWLINE | section | key_value | list_item | text)* EOF

    section
        := SECTION_HEADER NEWLINE

    key_value
        := KEY COLON VALUE? NEWLINE

    list_item
        := LIST_ITEM NEWLINE

    text
        := TEXT NEWLINE

    Blank lines are ignored. Entries before the first section are attached
    directly to the document. Later entries are attached to the active section.
    """

    def __init__(self, tokens: Sequence[Token]) -> None:
        if isinstance(tokens, (str, bytes)) or not isinstance(tokens, Sequence):
            raise TypeError("tokens must be a sequence of Token objects.")

        self._tokens = tuple(tokens)
        self._validate_token_stream()
        self._index = 0
        self._current_section: SectionNode | None = None

    def parse(self) -> DocumentNode:
        """
        Parse the complete token stream into a fresh DocumentNode.

        Repeated calls are deterministic and return independent AST objects.
        """

        self._index = 0
        self._current_section = None

        first_token = self._tokens[0]

        document = DocumentNode(
            line=first_token.line,
            column=first_token.column,
            source_file=first_token.source_file,
        )

        while not self._check(TokenType.EOF):
            if self._match(TokenType.NEWLINE):
                continue

            if self._check(TokenType.SECTION_HEADER):
                self._parse_section(document)
                continue

            if self._check(TokenType.KEY):
                self._add_entry(
                    document,
                    self._parse_key_value(),
                )
                continue

            if self._check(TokenType.LIST_ITEM):
                self._add_entry(
                    document,
                    self._parse_list_item(),
                )
                continue

            if self._check(TokenType.TEXT):
                self._add_entry(
                    document,
                    self._parse_text(),
                )
                continue

            token = self._current()
            self._raise_syntax_error(
                f"Unexpected {token.type.name} token.",
                token,
            )

        self._advance()
        return document

    def _parse_section(self, document: DocumentNode) -> None:
        header = self._consume(
            TokenType.SECTION_HEADER,
            "Expected a section header.",
        )

        if not header.value.strip():
            self._raise_syntax_error(
                "Section header must not be empty.",
                header,
            )

        self._consume(
            TokenType.NEWLINE,
            "Expected NEWLINE after section header.",
        )

        section = SectionNode(
            name=header.value,
            line=header.line,
            column=header.column,
            source_file=header.source_file,
        )

        document.add_section(section)
        self._current_section = section

    def _parse_key_value(self) -> KeyValueNode:
        key_token = self._consume(
            TokenType.KEY,
            "Expected a key.",
        )

        if not key_token.value.strip():
            self._raise_syntax_error(
                "Key must not be empty.",
                key_token,
            )

        self._consume(
            TokenType.COLON,
            "Expected COLON after key.",
        )

        value = ""

        if self._check(TokenType.VALUE):
            value_token = self._advance()

            if not value_token.value.strip():
                self._raise_syntax_error(
                    "VALUE token must not be empty.",
                    value_token,
                )

            value = value_token.value

        self._consume(
            TokenType.NEWLINE,
            "Expected NEWLINE after key-value entry.",
        )

        return KeyValueNode(
            key=key_token.value,
            value=value,
            line=key_token.line,
            column=key_token.column,
            source_file=key_token.source_file,
        )

    def _parse_list_item(self) -> ListItemNode:
        token = self._consume(
            TokenType.LIST_ITEM,
            "Expected a list item.",
        )

        if not token.value.strip():
            self._raise_syntax_error(
                "List item must not be empty.",
                token,
            )

        self._consume(
            TokenType.NEWLINE,
            "Expected NEWLINE after list item.",
        )

        return ListItemNode(
            value=token.value,
            line=token.line,
            column=token.column,
            source_file=token.source_file,
        )

    def _parse_text(self) -> TextNode:
        token = self._consume(
            TokenType.TEXT,
            "Expected text.",
        )

        if not token.value.strip():
            self._raise_syntax_error(
                "Text must not be empty.",
                token,
            )

        self._consume(
            TokenType.NEWLINE,
            "Expected NEWLINE after text.",
        )

        return TextNode(
            value=token.value,
            line=token.line,
            column=token.column,
            source_file=token.source_file,
        )

    def _add_entry(
        self,
        document: DocumentNode,
        entry: ASTNode,
    ) -> None:
        if self._current_section is None:
            document.add_entry(entry)
            return

        self._current_section.add_entry(entry)

    def _current(self) -> Token:
        return self._tokens[self._index]

    def _check(self, token_type: TokenType) -> bool:
        return self._current().type is token_type

    def _match(self, token_type: TokenType) -> bool:
        if not self._check(token_type):
            return False

        self._advance()
        return True

    def _advance(self) -> Token:
        token = self._current()

        if self._index < len(self._tokens) - 1:
            self._index += 1

        return token

    def _consume(
        self,
        token_type: TokenType,
        message: str,
    ) -> Token:
        if self._check(token_type):
            return self._advance()

        self._raise_syntax_error(message, self._current())

    @staticmethod
    def _raise_syntax_error(
        message: str,
        token: Token,
    ) -> None:
        raise SpecificationSyntaxError(
            message,
            line=token.line,
            column=token.column,
            source_file=token.source_file,
        )

    def _validate_token_stream(self) -> None:
        if not self._tokens:
            raise SpecificationTokenStreamError(
                "Token stream must contain at least one token."
            )

        eof_indices: list[int] = []

        for index, token in enumerate(self._tokens):
            if not isinstance(token, Token):
                raise SpecificationTokenStreamError(
                    f"tokens[{index}] must be a Token."
                )

            if not isinstance(token.type, TokenType):
                raise SpecificationTokenStreamError(
                    f"tokens[{index}].type must be a TokenType."
                )

            if not isinstance(token.value, str):
                raise SpecificationTokenStreamError(
                    f"tokens[{index}].value must be a string."
                )

            if type(token.line) is not int or token.line < 1:
                raise SpecificationTokenStreamError(
                    f"tokens[{index}].line must be an integer "
                    "greater than or equal to 1."
                )

            if type(token.column) is not int or token.column < 1:
                raise SpecificationTokenStreamError(
                    f"tokens[{index}].column must be an integer "
                    "greater than or equal to 1."
                )

            if not isinstance(token.source_file, str):
                raise SpecificationTokenStreamError(
                    f"tokens[{index}].source_file must be a string."
                )

            if not isinstance(token.section, str):
                raise SpecificationTokenStreamError(
                    f"tokens[{index}].section must be a string."
                )

            if token.type is TokenType.EOF:
                eof_indices.append(index)

        if len(eof_indices) != 1:
            raise SpecificationTokenStreamError(
                "Token stream must contain exactly one EOF token."
            )

        if eof_indices[0] != len(self._tokens) - 1:
            raise SpecificationTokenStreamError(
                "EOF token must be the final token in the stream."
            )
