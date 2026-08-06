"""
SystemVerilog signal declaration parser.
"""

from app.ast.signal_declaration import SignalDeclaration

from app.domain.rtl_tokens import RTLTokenType

from app.parsers.rtl.parser_context import ParserContext

from app.parsers.rtl.parsers.base_parser import BaseParser
from app.parsers.rtl.parsers.packed_range_parser import PackedRangeParser


class SignalParser(BaseParser):

    _SIGNAL_TYPES = {
        "logic",
        "wire",
        "reg",
        "bit",
    }

    @staticmethod
    def matches(
        context: ParserContext,
    ):

        if context.eof():
            return False

        token = context.current()

        return (
            token.token_type == RTLTokenType.KEYWORD
            and token.value in SignalParser._SIGNAL_TYPES
        )

    @staticmethod
    def parse(
        context: ParserContext,
    ):

        #
        # logic / wire / reg / bit
        #
        token = context.current()

        signal_type = context.advance().value

        #
        # Optional packed range
        #
        packed_range = None

        if PackedRangeParser.matches(
            context,
        ):

            packed_range = PackedRangeParser.parse(
                context,
            )

        #
        # Identifier
        #
        if (
            context.eof()
            or context.current().token_type != RTLTokenType.IDENTIFIER
        ):
            raise RuntimeError(
                "Expected signal identifier."
            )

        name = context.advance().value

        #
        # Optional ';'
        #
        if (
            not context.eof()
            and context.current().value == ";"
        ):
            context.advance()

        node = SignalDeclaration(
            signal_type=signal_type,
            packed_range=packed_range,
            name=name,
        )

        object.__setattr__(
            node,
            "location",
            token.source_location,
        )

        return node

