from app.domain.rtl_tokens import RTLToken
from app.domain.rtl_tokens import RTLTokenType
from app.engines.diagnostics.diagnostic_factory import (
    LexerDiagnosticFactory,
)
from app.parsers.rtl.character_stream import CharacterStream


class StringReader:
    """
    Reads SystemVerilog string literals.

    Version 2:
        - deterministic diagnostics
        - no exceptions
    """

    @staticmethod
    def matches(
        stream: CharacterStream,
    ) -> bool:

        if stream.eof():
            return False

        return stream.peek() == '"'

    @staticmethod
    def read(
        stream: CharacterStream,
        diagnostics,
    ) -> RTLToken:

        location = stream.location()

        stream.advance()

        characters: list[str] = []

        while (
            not stream.eof()
            and stream.peek() != '"'
        ):
            characters.append(
                stream.advance()
            )

        if stream.eof():

            diagnostics.append(
                LexerDiagnosticFactory.unterminated_string(
                    location
                )
            )

            return RTLToken(
                token_type=RTLTokenType.STRING,
                value="".join(characters),
                source_location=location,
            )

        stream.advance()

        return RTLToken(
            token_type=RTLTokenType.STRING,
            value="".join(characters),
            source_location=location,
        )
