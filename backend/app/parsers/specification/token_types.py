from enum import Enum


class TokenType(str, Enum):
    """
    Generic document tokens.

    The lexer understands document structure.

    The parser understands engineering meaning.
    """

    # document

    SECTION_HEADER = "SECTION_HEADER"

    KEY = "KEY"

    VALUE = "VALUE"

    TEXT = "TEXT"

    LIST_ITEM = "LIST_ITEM"

    IDENTIFIER = "IDENTIFIER"

    NUMBER = "NUMBER"

    BOOLEAN = "BOOLEAN"

    STRING = "STRING"

    COLON = "COLON"

    DASH = "DASH"

    COMMA = "COMMA"

    NEWLINE = "NEWLINE"

    EOF = "EOF"
