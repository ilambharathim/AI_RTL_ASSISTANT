"""
SystemVerilog if statement parser.
"""

from app.ast.if_statement import IfStatement
from app.parsers.rtl.parser_context import ParserContext
from app.parsers.rtl.parsers.base_parser import BaseParser
from app.parsers.rtl.parsers.statement_parser import StatementParser
from app.domain.rtl_tokens import RTLTokenType


class IfParser(BaseParser):

    @staticmethod
    def matches(
        context: ParserContext,
    ) -> bool:

        if context.eof():
            return False

        token = context.current()

        return (
            token.token_type == RTLTokenType.KEYWORD
            and token.value == "if"
        )

    @staticmethod
    def parse(
        context: ParserContext,
    ) -> IfStatement:

        #
        # if
        #
        context.advance()

        #
        # (
        #
        if (
            context.current().token_type == RTLTokenType.SYMBOL
            and context.current().value == "("
        ):
            context.advance()

        #
        # condition
        #
        condition = []

        while not context.eof():

            token = context.current()

            if (
                token.token_type == RTLTokenType.SYMBOL
                and token.value == ")"
            ):
                context.advance()
                break

            condition.append(token.value)

            context.advance()

        #
        # then statement
        #
        then_branch = []

        if StatementParser.matches(context):

            then_branch.append(
                StatementParser.parse(context)
            )

        #
        # optional else
        #
        else_branch = []

        if (
            not context.eof()
            and context.current().token_type == RTLTokenType.KEYWORD
            and context.current().value == "else"
        ):

            context.advance()

            if StatementParser.matches(context):

                else_branch.append(
                    StatementParser.parse(context)
                )

        node = IfStatement(
            condition=" ".join(condition),
            then_branch=tuple(then_branch),
            else_branch=tuple(else_branch),
        )

        object.__setattr__(
            node,
            "location",
            token.source_location,
        )

        return node
