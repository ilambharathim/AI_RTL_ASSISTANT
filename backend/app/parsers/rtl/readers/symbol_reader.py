from app.domain.rtl_tokens import RTLToken, RTLTokenType
from app.language.systemverilog.symbols import SYSTEMVERILOG_SYMBOLS
from app.parsers.rtl.character_stream import CharacterStream


class SymbolReader:
    """
    Reads SystemVerilog punctuation symbols.
    """

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
    ) -> RTLToken:

        location = stream.location()

        value = stream.advance()

        return RTLToken(
            token_type=RTLTokenType.SYMBOL,
            value=value,
            source_location=location,
        )
