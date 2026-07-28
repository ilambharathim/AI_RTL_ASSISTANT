from enum import Enum


class RTLTokenType(str, Enum):
    """
    Deterministic RTL lexer token types.

    Every token produced by the RTL lexer belongs to one of these
    categories. This enum is intentionally stable because parser
    behavior depends upon deterministic token classification.
    """

    IDENTIFIER = "IDENTIFIER"
    KEYWORD = "KEYWORD"
    NUMBER = "NUMBER"
    STRING = "STRING"

    SYMBOL = "SYMBOL"
    OPERATOR = "OPERATOR"

    COMMENT = "COMMENT"
    WHITESPACE = "WHITESPACE"

    END_OF_FILE = "END_OF_FILE"

