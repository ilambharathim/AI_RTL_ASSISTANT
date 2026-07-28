from app.domain.rtl_tokens import RTLToken, RTLTokenType
from app.language.systemverilog.keywords import SYSTEMVERILOG_KEYWORDS
from app.parsers.rtl.character_stream import CharacterStream


class IdentifierReader:
    """
    Reads SystemVerilog identifiers and reserved keywords.
    """

    @staticmethod
    def matches(
        stream: CharacterStream,
    ) -> bool:
        if stream.eof():
            return False

        character = stream.peek()

        return (
            character == "_"
            or character.isalpha()
        )

    @staticmethod
    def read(
        stream: CharacterStream,
    ) -> RTLToken:

        location = stream.location()

        characters: list[str] = []

        while (
            not stream.eof()
            and IdentifierReader._is_identifier_continue(
                stream.peek()
            )
        ):
            characters.append(
                stream.advance()
            )

        value = "".join(characters)

        token_type = (
            RTLTokenType.KEYWORD
            if value in SYSTEMVERILOG_KEYWORDS
            else RTLTokenType.IDENTIFIER
        )

        return RTLToken(
            token_type=token_type,
            value=value,
            source_location=location,
        )

    @staticmethod
    def _is_identifier_continue(
        character: str,
    ) -> bool:
        return (
            character == "_"
            or character == "$"
            or character.isalpha()
            or character.isdigit()
        )
