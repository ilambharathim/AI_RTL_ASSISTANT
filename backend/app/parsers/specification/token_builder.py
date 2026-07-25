"""
RIVA Token Builder

Creates validated Token objects.
"""

from app.parsers.specification.tokens import Token
from app.parsers.specification.token_types import TokenType


class TokenBuilder:
    """
    Responsible for creating validated Token objects.
    """

    @staticmethod
    def build(
        token_type: TokenType,
        value: str,
        line: int,
        column: int,
        source_file: str | None = None,
        section: str | None = None,
    ) -> Token:

        if not isinstance(token_type, TokenType):
            raise TypeError("token_type must be a TokenType.")

        if line < 1:
            raise ValueError("line number must be >= 1")

        if column < 1:
            raise ValueError("column number must be >= 1")

        return Token(
            type=token_type,
            value=value,
            line=line,
            column=column,
            source_file=source_file,
            section=section,
        )