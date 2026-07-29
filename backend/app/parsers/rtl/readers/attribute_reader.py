from app.domain.rtl_tokens import RTLToken
from app.domain.rtl_tokens import RTLTokenType
from app.engines.diagnostics.diagnostic_factory import (
    LexerDiagnosticFactory,
)
from app.parsers.rtl.character_stream import CharacterStream


class AttributeReader:
    """
    Reads SystemVerilog attribute blocks.

    Example:

        (* keep *)

        (* ram_style = "block" *)
    """

    @staticmethod
    def matches(
        stream: CharacterStream,
    ) -> bool:

        if stream.eof():
            return False

        remaining = stream.source[stream.index:]

        return remaining.startswith("(*")

    @staticmethod
    def read(
        stream: CharacterStream,
        diagnostics,
    ) -> RTLToken:

        location = stream.location()

        stream.advance()
        stream.advance()

        characters: list[str] = []

        while not stream.eof():

            remaining = stream.source[stream.index:]

            if remaining.startswith("*)"):

                stream.advance()
                stream.advance()

                return RTLToken(
                    token_type=RTLTokenType.ATTRIBUTE,
                    value="".join(characters).strip(),
                    source_location=location,
                )

            characters.append(
                stream.advance()
            )

        diagnostics.append(
            LexerDiagnosticFactory.unknown_character(
                location,
                "unterminated attribute",
            )
        )

        return RTLToken(
            token_type=RTLTokenType.ATTRIBUTE,
            value="".join(characters).strip(),
            source_location=location,
        )
