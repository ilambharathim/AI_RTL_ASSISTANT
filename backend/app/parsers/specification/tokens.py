"""
Token model for the RIVA specification compiler frontend.
"""

from dataclasses import dataclass

from app.parsers.specification.token_types import TokenType


@dataclass(slots=True)
class Token:
    """
    Generic document token produced by the lexer.

    Engineering meaning is intentionally not encoded in this model. Tokens
    preserve generic document structure, source location, source filename,
    and the active document section.
    """

    type: TokenType
    value: str
    line: int
    column: int
    source_file: str = ""
    section: str = ""

    def __str__(self) -> str:
        """
        Return a stable single-line diagnostic representation.

        ``repr`` formatting keeps control characters such as newlines,
        tabs, and carriage returns escaped instead of printing them directly.
        """

        return (
            f"{self.type.name:<18}"
            f"value={self.value!r} "
            f"(line={self.line}, column={self.column})"
        )
