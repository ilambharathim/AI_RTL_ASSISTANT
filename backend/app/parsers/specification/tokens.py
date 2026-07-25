from dataclasses import dataclass

from app.parsers.specification.token_types import TokenType


@dataclass(slots=True)
class Token:
    """
    Generic document token.

    Produced by the lexer.

    Consumed by the parser.
    """

    type: TokenType

    value: str

    line: int

    column: int

    source_file: str = ""

    section: str = ""

    def __str__(self) -> str:
        return (
            f"{self.type.name:<18}"
            f"value='{self.value}' "
            f"(line={self.line}, column={self.column})"
        )
