from app.domain.rtl_tokens import RTLToken
from app.domain.rtl_tokens import RTLTokenType
from app.engines.diagnostics.diagnostic_factory import (
    LexerDiagnosticFactory,
)
from app.parsers.rtl.character_stream import CharacterStream


class NumberReader:
    """
    Reads SystemVerilog numeric literals.

    Version 4:
        - decimal integers
        - based integers
        - signed based integers
        - deterministic diagnostics
    """

    _BASE_SPECIFIERS = {
        "b", "B",
        "o", "O",
        "d", "D",
        "h", "H",
    }

    @staticmethod
    def matches(
        stream: CharacterStream,
    ) -> bool:

        if stream.eof():
            return False

        return (
            stream.peek().isdigit()
            or stream.peek() == "'"
        )

    @staticmethod
    def read(
        stream: CharacterStream,
        diagnostics,
    ) -> RTLToken:

        location = stream.location()

        characters: list[str] = []

        while (
            not stream.eof()
            and stream.peek().isdigit()
        ):
            characters.append(stream.advance())

        if (
            not stream.eof()
            and stream.peek() == "'"
        ):

            characters.append(stream.advance())

            if (
                not stream.eof()
                and stream.peek() in ("s", "S")
            ):
                characters.append(stream.advance())

            if (
                stream.eof()
                or stream.peek()
                not in NumberReader._BASE_SPECIFIERS
            ):

                diagnostics.append(
                    LexerDiagnosticFactory.invalid_based_literal(
                        location
                    )
                )

                return RTLToken(
                    token_type=RTLTokenType.NUMBER,
                    value="".join(characters),
                    source_location=location,
                )

            characters.append(stream.advance())

            while (
                not stream.eof()
                and (
                    stream.peek().isalnum()
                    or stream.peek() == "_"
                )
            ):
                characters.append(stream.advance())

        return RTLToken(
            token_type=RTLTokenType.NUMBER,
            value="".join(characters),
            source_location=location,
        )
