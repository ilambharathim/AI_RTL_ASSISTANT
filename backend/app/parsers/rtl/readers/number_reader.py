from app.domain.rtl_tokens import RTLToken
from app.domain.rtl_tokens import RTLTokenType
from app.parsers.rtl.character_stream import CharacterStream


class NumberReader:
    """
    Reads decimal integer literals.

    Future milestones will extend this reader to support
    based literals, real numbers and time literals.
    """

    @staticmethod
    def matches(
        stream: CharacterStream,
    ) -> bool:
        if stream.eof():
            return False

        return stream.peek().isdigit()

    @staticmethod
    def read(
        stream: CharacterStream,
    ) -> RTLToken:

        location = stream.location()

        digits: list[str] = []

        while (
            not stream.eof()
            and stream.peek().isdigit()
        ):
            digits.append(
                stream.advance()
            )

        return RTLToken(
            token_type=RTLTokenType.NUMBER,
            value="".join(digits),
            source_location=location,
        )
