"""
Specification Lexer

Converts normalized specification text into
generic document tokens.
"""

from app.parsers.specification.tokens import Token
from app.parsers.specification.token_types import TokenType


class SpecificationLexer:

    def __init__(self, text: str, source_file: str = ""):

        self.text = text
        self.source_file = source_file

        self.position = 0
        self.line = 1
        self.column = 1

        self.length = len(text)

        self.current_char = text[0] if self.length else None

    # ---------------------------------------------------------

    def advance(self):

        if self.current_char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        self.position += 1

        if self.position >= self.length:
            self.current_char = None
        else:
            self.current_char = self.text[self.position]

    # ---------------------------------------------------------

    def peek(self):

        nxt = self.position + 1

        if nxt >= self.length:
            return None

        return self.text[nxt]

    # ---------------------------------------------------------

    def skip_whitespace(self):

        while self.current_char is not None:

            if self.current_char in (" ", "\t"):
                self.advance()
            else:
                break

    # ---------------------------------------------------------

    def create_token(self, token_type, value):

        return Token(
            type=token_type,
            value=value,
            line=self.line,
            column=self.column,
            source_file=self.source_file,
        )

    # ---------------------------------------------------------

    def read_line(self):
        """
        Read one logical line.

        Stops at newline but does not consume
        the next line.
        """

        chars = []

        while self.current_char is not None:

            if self.current_char == "\n":
                break

            chars.append(self.current_char)

            self.advance()

        return "".join(chars).strip()

    # ---------------------------------------------------------

    def tokenize(self):

        tokens = []

        while self.current_char is not None:

            self.skip_whitespace()

            if self.current_char is None:
                break

            #
            # Skip blank lines
            #

            if self.current_char == "\n":
                self.advance()
                continue

            line = self.read_line()

            print(f"LINE --> {line}")

            #
            # consume newline
            #

            if self.current_char == "\n":
                self.advance()

        tokens.append(
            self.create_token(
                TokenType.EOF,
                ""
            )
        )

        return tokens
