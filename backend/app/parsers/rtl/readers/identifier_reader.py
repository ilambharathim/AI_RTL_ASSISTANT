from app.domain.rtl_tokens import RTLToken
from app.domain.rtl_tokens import RTLTokenType
from app.language.systemverilog.keywords import SYSTEMVERILOG_KEYWORDS
from app.parsers.rtl.character_stream import CharacterStream


class IdentifierReader:
    """
    Reads SystemVerilog identifiers.

    Supports:
        - normal identifiers
        - escaped identifiers
    """

    @staticmethod
    def matches(
        stream: CharacterStream,
    ) -> bool:

        if stream.eof():
            return False

        character = stream.peek()

        return (
            character.isalpha()
            or character == "_"
            or character == "$"
            or character == "\\"
        )

    @staticmethod
    def read(
        stream: CharacterStream,
        diagnostics,
    ) -> RTLToken:

        location = stream.location()

        if stream.peek() == "\\":

            stream.advance()

            characters: list[str] = []

            while (
                not stream.eof()
                and not stream.peek().isspace()
            ):
                characters.append(
                    stream.advance()
                )

            return RTLToken(
                token_type=RTLTokenType.IDENTIFIER,
                value="\\" + "".join(characters),
                source_location=location,
            )

        characters: list[str] = []

        while (
            not stream.eof()
            and (
                stream.peek().isalnum()
                or stream.peek() in ("_", "$")
            )
        ):
            characters.append(
                stream.advance()
            )

        identifier = "".join(characters)

        token_type = (
            RTLTokenType.KEYWORD
            if identifier in SYSTEMVERILOG_KEYWORDS
            else RTLTokenType.IDENTIFIER
        )

        return RTLToken(
            token_type=token_type,
            value=identifier,
            source_location=location,
        )
