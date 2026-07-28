from app.engines.diagnostics.diagnostic_factory import (
    LexerDiagnosticFactory,
)
from app.parsers.rtl.character_stream import CharacterStream


class CommentReader:
    """
    Reads and discards SystemVerilog comments.

    Version 3:
        - //
        - /* */
        - deterministic diagnostics
    """

    @staticmethod
    def matches(
        stream: CharacterStream,
    ) -> bool:

        if stream.eof():
            return False

        remaining = stream.source[stream.index:]

        return (
            remaining.startswith("//")
            or remaining.startswith("/*")
        )

    @staticmethod
    def read(
        stream: CharacterStream,
        diagnostics,
    ) -> None:

        remaining = stream.source[stream.index:]

        #
        # Single-line comment
        #
        if remaining.startswith("//"):

            while (
                not stream.eof()
                and stream.peek() != "\n"
            ):
                stream.advance()

            return

        #
        # Block comment
        #
        location = stream.location()

        stream.advance()
        stream.advance()

        while not stream.eof():

            if (
                stream.peek() == "*"
                and stream.index + 1 < len(stream.source)
                and stream.source[stream.index + 1] == "/"
            ):
                stream.advance()
                stream.advance()
                return

            stream.advance()

        diagnostics.append(
            LexerDiagnosticFactory.unterminated_block_comment(
                location
            )
        )
