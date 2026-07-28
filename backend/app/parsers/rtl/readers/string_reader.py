from app.domain.rtl_tokens import RTLToken
from app.domain.rtl_tokens import RTLTokenType
from app.parsers.rtl.character_stream import CharacterStream


class StringReader:

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
            raise RuntimeError(
                "Unterminated string literal."
            )

        stream.advance()

        return RTLToken(
            token_type=RTLTokenType.STRING,
            value="".join(characters),
            source_location=location,
        )
