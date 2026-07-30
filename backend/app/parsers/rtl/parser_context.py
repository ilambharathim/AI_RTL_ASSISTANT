"""
Parser context.
"""

from app.domain.rtl_tokens import RTLToken


class ParserContext:

    def __init__(
        self,
        tokens: tuple[RTLToken, ...],
    ):

        self.tokens = tokens

        self.index = 0

    def current(self):

        return self.tokens[self.index]

    def advance(self):

        token = self.tokens[self.index]

        self.index += 1

        return token

    def eof(self):

        return (
            self.current().token_type.value
            == "END_OF_FILE"
        )
