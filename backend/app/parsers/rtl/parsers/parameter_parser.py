"""
SystemVerilog parameter declaration parser.
"""

from app.ast.parameter_declaration import ParameterDeclaration
from app.domain.rtl_tokens import RTLTokenType
from app.parsers.rtl.parser_context import ParserContext
from app.parsers.rtl.parsers.base_parser import BaseParser


class ParameterParser(BaseParser):

    @staticmethod
    def matches(
        context: ParserContext,
    ) -> bool:

        token = context.current()

        return (
            token.token_type == RTLTokenType.KEYWORD
            and token.value == "parameter"
        )

    @staticmethod
    def parse(
        context: ParserContext,
    ) -> ParameterDeclaration:

        #
        # parameter
        #
        context.advance()

        #
        # parameter name
        #
        name = context.advance()

        #
        # '='
        #
        if (
            context.current().token_type == RTLTokenType.OPERATOR
            and context.current().value == "="
        ):
            context.advance()

        #
        # parameter value
        #
        value = context.advance()

        #
        # skip until ';'
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

        return ParameterDeclaration(
            name=name.value,
            value=value.value,
        )
