from app.domain.rtl_tokens import RTLToken
from app.domain.rtl_tokens import RTLTokenType
from app.engines.diagnostics.diagnostic_factory import (
    LexerDiagnosticFactory,
)
from app.language.systemverilog.compiler_directives import (
    SYSTEMVERILOG_COMPILER_DIRECTIVES,
)
from app.parsers.rtl.character_stream import CharacterStream


class DirectiveReader:
    """
    Reads SystemVerilog compiler directives.
    """

    @staticmethod
    def matches(
        stream: CharacterStream,
    ) -> bool:

        return (
            not stream.eof()
            and stream.peek() == "`"
        )

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
            and (
                stream.peek().isalnum()
                or stream.peek() == "_"
            )
        ):
            characters.append(
                stream.advance()
            )

        directive = "".join(characters)

        if directive not in SYSTEMVERILOG_COMPILER_DIRECTIVES:

            diagnostics.append(
                LexerDiagnosticFactory.unknown_character(
                    location,
                    "`" + directive,
                )
            )

        return RTLToken(
            token_type=RTLTokenType.DIRECTIVE,
            value=directive,
            source_location=location,
        )
