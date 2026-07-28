from dataclasses import dataclass

from app.shared.source_location import SourceLocation


@dataclass(slots=True)
class CharacterStream:
    """
    Deterministic character reader for RTL source text.

    Maintains cursor position and source location information
    while the lexer consumes input.
    """

    source: str
    index: int = 0
    line: int = 1
    column: int = 1

    def __post_init__(self) -> None:
        if not isinstance(self.source, str):
            raise TypeError(
                "source must be a string."
            )

    def eof(self) -> bool:
        return self.index >= len(self.source)

    def peek(self) -> str:
        if self.eof():
            return ""

        return self.source[self.index]

    def advance(self) -> str:
        if self.eof():
            return ""

        character = self.source[self.index]

        self.index += 1

        if character == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        return character

    def location(self) -> SourceLocation:
        return SourceLocation(
            line=self.line,
            column=self.column,
        )
