from app.parsers.rtl.character_stream import CharacterStream


class CommentReader:
    """
    Reads and discards SystemVerilog comments.

    Version 1:
        - supports //
        - block comments will be added later
    """

    @staticmethod
    def matches(
        stream: CharacterStream,
    ) -> bool:

        if stream.eof():
            return False

        remaining = stream.source[stream.index:]

        return remaining.startswith("//")

    @staticmethod
    def read(
        stream: CharacterStream,
    ) -> None:

        while (
            not stream.eof()
            and stream.peek() != "\n"
        ):
            stream.advance()
