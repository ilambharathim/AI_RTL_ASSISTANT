"""
SystemVerilog signal declaration parser.
"""

from app.ast.signal_declaration import SignalDeclaration
from app.domain.rtl_tokens import RTLTokenType
from app.parsers.rtl.parser_context import ParserContext
from app.parsers.rtl.parsers.base_parser import BaseParser


class SignalParser(BaseParser):

    _SIGNAL_TYPES = {
        "logic",
        "wire",
        "reg",
    }

    @staticmethod
    def matches(
        context: ParserContext,
    ) -> bool:

        token = context.current()

        return (
            token.token_type == RTLTokenType.KEYWORD
            and token.value in SignalParser._SIGNAL_TYPES
        )

    @staticmethod
    def parse(
        context: ParserContext,
    ) -> SignalDeclaration:

        signal_type = context.advance().value

        identifier = context.advance()

        #
        # Skip until ';'
        #
        while not context.eof():

            token = context.current()

            if (
                token.token_type == RTLTokenType.SYMBOL
                and token.value == ";"
            ):
                context.advance()
                break

            context.advance()

        return SignalDeclaration(
            signal_type=signal_type,
            name=identifier.value,
        )
