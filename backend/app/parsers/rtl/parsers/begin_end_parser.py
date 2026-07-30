"""
SystemVerilog begin/end statement block parser.
"""

from app.ast.statement_block import StatementBlock
from app.domain.rtl_tokens import RTLTokenType
from app.parsers.rtl.parser_context import ParserContext
from app.parsers.rtl.parsers.base_parser import BaseParser


class BeginEndParser(BaseParser):

    @staticmethod
    def matches(
        context: ParserContext,
    ) -> bool:

        if context.eof():
            return False

        token = context.current()

        return (
            token.token_type == RTLTokenType.KEYWORD
            and token.value == "begin"
        )

    @staticmethod
    def parse(
        context: ParserContext,
    ) -> StatementBlock:

        #
        # Avoid circular imports
        #
        from app.parsers.rtl.parsers.statement_parser import (
            StatementParser,
        )

        #
        # begin
        #
        context.advance()

        statements = []

        while not context.eof():

            token = context.current()

            if (
                token.token_type == RTLTokenType.KEYWORD
                and token.value == "end"
            ):
                context.advance()
                break

            if StatementParser.matches(context):

                statements.append(
                    StatementParser.parse(context)
                )

                continue

            context.advance()

        return StatementBlock(
            statements=tuple(statements),
        )
