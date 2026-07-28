from app.domain.rtl_tokens import RTLToken, RTLTokenType
from app.parsers.rtl.character_stream import CharacterStream
from app.parsers.rtl.lexer_result import RTLLexerResult
from app.parsers.rtl.readers.identifier_reader import IdentifierReader
from app.parsers.rtl.readers.number_reader import NumberReader
from app.parsers.rtl.readers.symbol_reader import SymbolReader


class RTLLexer:
    """
    Deterministic RTL lexer.

    Version 5:
        - whitespace
        - identifiers
        - keywords
        - decimal integers
        - symbols
        - EOF
    """

    def tokenize(
        self,
        source: str,
    ) -> RTLLexerResult:

        stream = CharacterStream(source)

        tokens: list[RTLToken] = []

        while not stream.eof():

            self._skip_whitespace(stream)

            if stream.eof():
                break

            if IdentifierReader.matches(stream):
                tokens.append(
                    IdentifierReader.read(stream)
                )
                continue

            if NumberReader.matches(stream):
                tokens.append(
                    NumberReader.read(stream)
                )
                continue

            if SymbolReader.matches(stream):
                tokens.append(
                    SymbolReader.read(stream)
                )
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
            diagnostics=(),
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
