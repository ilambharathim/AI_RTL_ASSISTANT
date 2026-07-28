from app.domain.rtl_tokens import RTLToken, RTLTokenType
from app.language.systemverilog.keywords import SYSTEMVERILOG_KEYWORDS
from app.language.systemverilog.symbols import SYSTEMVERILOG_SYMBOLS
from app.parsers.rtl.character_stream import CharacterStream
from app.parsers.rtl.lexer_result import RTLLexerResult


class RTLLexer:
    """
    Deterministic RTL lexer.

    Version 3:
        - skips whitespace
        - recognizes identifiers
        - recognizes SystemVerilog keywords
        - recognizes punctuation symbols
        - produces EOF token
    """

    def tokenize(self, source: str) -> RTLLexerResult:
        stream = CharacterStream(source)

        tokens: list[RTLToken] = []

        while not stream.eof():

            self._skip_whitespace(stream)

            if stream.eof():
                break

            character = stream.peek()

            if self._is_identifier_start(character):
                tokens.append(
                    self._lex_identifier_or_keyword(stream)
                )
                continue

            if character in SYSTEMVERILOG_SYMBOLS:
                tokens.append(
                    self._lex_symbol(stream)
                )
                continue

            raise NotImplementedError(
                f"Unsupported character: {character!r}"
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

    def _lex_identifier_or_keyword(
        self,
        stream: CharacterStream,
    ) -> RTLToken:

        location = stream.location()

        characters: list[str] = []

        while (
            not stream.eof()
            and self._is_identifier_continue(stream.peek())
        ):
            characters.append(stream.advance())

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

    def _lex_symbol(
        self,
        stream: CharacterStream,
    ) -> RTLToken:

        location = stream.location()

        value = stream.advance()

        return RTLToken(
            token_type=RTLTokenType.SYMBOL,
            value=value,
            source_location=location,
        )

    def _is_identifier_start(
        self,
        character: str,
    ) -> bool:
        return (
            character == "_"
            or character.isalpha()
        )

    def _is_identifier_continue(
        self,
        character: str,
    ) -> bool:
        return (
            character == "_"
            or character == "$"
            or character.isalpha()
            or character.isdigit()
        )
