"""
SystemVerilog packed range parser.

Parses:

    [expr : expr]
"""

from app.ast.packed_range import PackedRange

from app.domain.rtl_tokens import RTLTokenType

from app.parsers.rtl.parsers.base_parser import BaseParser
from app.parsers.rtl.parsers.expression_parser import ExpressionParser


class PackedRangeParser(BaseParser):

    @staticmethod
    def matches(context):

        return (
            not context.eof()
            and context.current().token_type == RTLTokenType.SYMBOL
            and context.current().value == "["
        )

    @staticmethod
    def parse(context):
        token = context.current()

        #
        # [
        #
        context.advance()

        left = ExpressionParser.parse(
            context,
        )

        #
        # :
        #
        if (
            context.eof()
            or context.current().value != ":"
        ):
            raise RuntimeError(
                "Expected ':' in packed range."
            )

        context.advance()

        right = ExpressionParser.parse(
            context,
        )

        #
        # ]
        #
        if (
            context.eof()
            or context.current().value != "]"
        ):
            raise RuntimeError(
                "Expected ']'."
            )

        context.advance()

        node = PackedRange(
            left,
            right,
        )

        object.__setattr__(
            node,
            "location",
            token.source_location,
        )

        return node

