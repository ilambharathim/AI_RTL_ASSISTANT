from app.domain.rtl_tokens import RTLToken
from app.domain.rtl_tokens import RTLTokenType
from app.parsers.rtl.character_stream import CharacterStream


class NumberReader:
    """
    Reads SystemVerilog numeric literals.

    Version 2:
        - decimal integers
        - based integers
    """

    _BASE_SPECIFIERS = {
        "b",
        "B",
        "o",
        "O",
        "d",
        "D",
        "h",
        "H",
    }

    @staticmethod
    def matches(
        stream: CharacterStream,
    ) -> bool:

        if stream.eof():
            return False

        character = stream.peek()

        return (
            character.isdigit()
            or character == "'"
        )

    @staticmethod
    def read(
        stream: CharacterStream,
    ) -> RTLToken:

        location = stream.location()

        characters: list[str] = []

        #
        # Optional size
        #
        while (
            not stream.eof()
            and stream.peek().isdigit()
        ):
            characters.append(
                stream.advance()
            )

        #
        # Based literal
        #
        if (
            not stream.eof()
            and stream.peek() == "'"
        ):

            characters.append(
                stream.advance()
            )

            if (
                stream.eof()
                or stream.peek()
                not in NumberReader._BASE_SPECIFIERS
            ):
                raise RuntimeError(
                    "Invalid based literal."
                )

            characters.append(
                stream.advance()
            )

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

        return RTLToken(
            token_type=RTLTokenType.NUMBER,
            value="".join(characters),
            source_location=location,
        )
