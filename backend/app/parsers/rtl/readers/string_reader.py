from app.domain.rtl_tokens import RTLToken
from app.domain.rtl_tokens import RTLTokenType
from app.engines.diagnostics.diagnostic_factory import (
    LexerDiagnosticFactory,
)
from app.parsers.rtl.character_stream import CharacterStream


class StringReader:
    """
    Reads SystemVerilog string literals.

    Supports:
        - Standard escape sequences
        - Diagnostic recovery for unterminated strings
    """

    _ESCAPES = {
        "n": "\n",
        "t": "\t",
        "\\": "\\",
        '"': '"',
    }

    @staticmethod
    def matches(
        stream: CharacterStream,
    ) -> bool:
        return (
            not stream.eof()
            and stream.peek() == '"'
        )

    @staticmethod
    def read(
        stream: CharacterStream,
        diagnostics,
    ) -> RTLToken:

        location = stream.location()

        stream.advance()

        characters: list[str] = []

        while not stream.eof():

            character = stream.advance()

            #
            # Closing quote
            #
            if character == '"':
                return RTLToken(
                    token_type=RTLTokenType.STRING,
                    value="".join(characters),
                    source_location=location,
                )

            #
            # Escape sequence
            #
            if character == "\\":

                if stream.eof():

                    diagnostics.append(
                        LexerDiagnosticFactory.unknown_character(
                            location,
                            "unterminated escape sequence",
                        )
                    )

                    break

                escape = stream.advance()

                if escape in StringReader._ESCAPES:
                    characters.append(
                        StringReader._ESCAPES[escape]
                    )
                else:

                    diagnostics.append(
                        LexerDiagnosticFactory.unknown_character(
                            location,
                            f"unknown escape '\\{escape}'",
                        )
                    )

                    characters.append(escape)

                continue

            characters.append(character)

        diagnostics.append(
            LexerDiagnosticFactory.unknown_character(
                location,
                "unterminated string literal",
            )
        )

        return RTLToken(
            token_type=RTLTokenType.STRING,
            value="".join(characters),
            source_location=location,
        )
