from app.domain.rtl_tokens import RTLToken
from app.domain.rtl_tokens import RTLTokenType
from app.parsers.rtl.character_stream import CharacterStream
from app.parsers.rtl.lexer_result import RTLLexerResult
from app.parsers.rtl.readers.reader_registry import READERS


class RTLLexer:
    """
    Deterministic RTL lexer.
    """

    def tokenize(
        self,
        source: str,
    ) -> RTLLexerResult:

        stream = CharacterStream(source)

        tokens: list[RTLToken] = []
        diagnostics = []

        while not stream.eof():

            self._skip_whitespace(stream)

            if stream.eof():
                break

            matched = False

            for reader in READERS:

                if reader.matches(stream):

                    token = reader.read(
                        stream,
                        diagnostics,
                    )

                    if token is not None:
                        tokens.append(token)

                    matched = True
                    break

            if matched:
                continue

            raise NotImplementedError(
                f"Unsupported character: {stream.peek()!r}"
            )

        tokens.append(
            RTLToken(
                token_type=RTLTokenType.END_OF_FILE,
                value="",
                source_location=stream.location(),
            )
        )

        return RTLLexerResult(
            tokens=tuple(tokens),
            diagnostics=tuple(diagnostics),
        )

    def _skip_whitespace(
        self,
        stream: CharacterStream,
    ) -> None:

        while (
            not stream.eof()
            and stream.peek().isspace()
        ):
            stream.advance()
