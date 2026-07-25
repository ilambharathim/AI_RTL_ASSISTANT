"""
Generic Character Scanner for RIVA

Reusable across all future parsers.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Position:
    index: int
    line: int
    column: int


class Scanner:

    def __init__(self, text: str):

        self.text = text

        self.length = len(text)

        self.index = 0

        self.line = 1

        self.column = 1

        self.current = text[0] if self.length else None

    # ----------------------------------------------------

    def eof(self):

        return self.current is None

    # ----------------------------------------------------

    def position(self):

        return Position(
            self.index,
            self.line,
            self.column,
        )

    # ----------------------------------------------------

    def save_state(self):

        return Position(
            self.index,
            self.line,
            self.column,
        )

    # ----------------------------------------------------

    def restore_state(self, pos: Position):

        self.index = pos.index
        self.line = pos.line
        self.column = pos.column

        if self.index >= self.length:
            self.current = None
        else:
            self.current = self.text[self.index]

    # ----------------------------------------------------

    def peek(self, offset: int = 1):

        idx = self.index + offset

        if idx >= self.length:
            return None

        return self.text[idx]

    # ----------------------------------------------------

    def advance(self):

        if self.current is None:
            return

        if self.current == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        self.index += 1

        if self.index >= self.length:
            self.current = None
        else:
            self.current = self.text[self.index]
