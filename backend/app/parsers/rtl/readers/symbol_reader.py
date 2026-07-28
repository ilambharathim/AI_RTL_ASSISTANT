from app.domain.rtl_tokens import RTLToken
from app.domain.rtl_tokens import RTLTokenType
from app.language.systemverilog.symbols import SYSTEMVERILOG_SYMBOLS
from app.parsers.rtl.character_stream import CharacterStream


class SymbolReader:

    @staticmethod
    def matches(
        stream: CharacterStream,
    ) -> bool:

        if stream.eof():
            return False

        return stream.peek() in SYSTEMVERILOG_SYMBOLS

    @staticmethod
    def read(
        stream: CharacterStream,
        diagnostics,
    ) -> RTLToken:

        location = stream.location()

        value = stream.advance()

        return RTLToken(
            token_type=RTLTokenType.SYMBOL,
            value=value,
            source_location=location,
        )
