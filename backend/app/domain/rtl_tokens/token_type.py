from enum import Enum


class RTLTokenType(str, Enum):
    """
    Deterministic RTL lexer token types.
    """

    IDENTIFIER = "IDENTIFIER"
    SYSTEM_IDENTIFIER = "SYSTEM_IDENTIFIER"

    KEYWORD = "KEYWORD"

    NUMBER = "NUMBER"
    REAL_NUMBER = "REAL_NUMBER"
    TIME_LITERAL = "TIME_LITERAL"

    STRING = "STRING"

    DIRECTIVE = "DIRECTIVE"
    ATTRIBUTE = "ATTRIBUTE"

    SYMBOL = "SYMBOL"
    OPERATOR = "OPERATOR"

    COMMENT = "COMMENT"
    WHITESPACE = "WHITESPACE"

    END_OF_FILE = "END_OF_FILE"
