"""
Continuous assignment parser.
"""

from app.ast.continuous_assign import ContinuousAssign
from app.domain.rtl_tokens import RTLTokenType
from app.parsers.rtl.parser_context import ParserContext
from app.parsers.rtl.parsers.base_parser import BaseParser


class AssignParser(BaseParser):

    @staticmethod
    def matches(
        context: ParserContext,
    ) -> bool:

        token = context.current()

        return (
            token.token_type == RTLTokenType.KEYWORD
            and token.value == "assign"
        )

    @staticmethod
    def parse(
        context: ParserContext,
    ) -> ContinuousAssign:

        #
        # assign
        #
        context.advance()

        #
        # target
        #
        target = context.advance()

        #
        # =
        #
        context.advance()

        expression_tokens = []

        while not context.eof():

            token = context.current()

            if (
                token.token_type == RTLTokenType.SYMBOL
                and token.value == ";"
            ):
                context.advance()
                break

            expression_tokens.append(
                token.value
            )

            context.advance()

        return ContinuousAssign(
            target=target.value,
            expression=" ".join(expression_tokens),
        )
