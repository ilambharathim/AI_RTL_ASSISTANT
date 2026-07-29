from enum import Enum


class RTLTokenType(str, Enum):
    """
    Deterministic RTL lexer token types.
    """

    IDENTIFIER = "IDENTIFIER"
    KEYWORD = "KEYWORD"

    NUMBER = "NUMBER"
    REAL_NUMBER = "REAL_NUMBER"
    TIME_LITERAL = "TIME_LITERAL"

    STRING = "STRING"

    DIRECTIVE = "DIRECTIVE"

    SYMBOL = "SYMBOL"
    OPERATOR = "OPERATOR"

    COMMENT = "COMMENT"
    WHITESPACE = "WHITESPACE"

    END_OF_FILE = "END_OF_FILE"
