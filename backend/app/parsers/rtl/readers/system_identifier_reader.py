from app.domain.rtl_tokens import RTLToken
from app.domain.rtl_tokens import RTLTokenType
from app.language.systemverilog.system_identifiers import (
    SYSTEMVERILOG_SYSTEM_IDENTIFIERS,
)
from app.parsers.rtl.character_stream import CharacterStream


class SystemIdentifierReader:
    """
    Reads SystemVerilog system tasks and system functions.

    Examples:
        $display
        $finish
        $clog2
        $bits
    """

    @staticmethod
    def matches(
        stream: CharacterStream,
    ) -> bool:

        return (
            not stream.eof()
            and stream.peek() == "$"
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

        identifier = "".join(characters)

        token_type = (
            RTLTokenType.SYSTEM_IDENTIFIER
            if identifier in SYSTEMVERILOG_SYSTEM_IDENTIFIERS
            else RTLTokenType.IDENTIFIER
        )

        return RTLToken(
            token_type=token_type,
            value="$" + identifier,
            source_location=location,
        )
