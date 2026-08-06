"""
SystemVerilog case statement parser.
"""

from app.ast.case_statement import CaseItem, CaseStatement
from app.domain.rtl_tokens import RTLTokenType
from app.parsers.rtl.parser_context import ParserContext
from app.parsers.rtl.parsers.base_parser import BaseParser
from app.parsers.rtl.parsers.statement_parser import StatementParser


class CaseParser(BaseParser):

    @staticmethod
    def matches(
        context: ParserContext,
    ) -> bool:

        if context.eof():
            return False

        token = context.current()

        return (
            token.token_type == RTLTokenType.KEYWORD
            and token.value == "case"
        )

    @staticmethod
    def parse(
        context: ParserContext,
    ) -> CaseStatement:

        #
        # case
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

        expression = []

        while not context.eof():

            token = context.current()

            if (
                token.token_type == RTLTokenType.SYMBOL
                and token.value == ")"
            ):
                context.advance()
                break

            expression.append(token.value)

            context.advance()

        items = []

        while not context.eof():

            token = context.current()

            if (
                token.token_type == RTLTokenType.KEYWORD
                and token.value == "endcase"
            ):
                context.advance()
                break

            #
            # label
            #
            label = token.value

            context.advance()

            #
            # :
            #
            if (
                not context.eof()
                and context.current().token_type == RTLTokenType.SYMBOL
                and context.current().value == ":"
            ):
                context.advance()

            statements = []

            if StatementParser.matches(context):

                statements.append(
                    StatementParser.parse(context)
                )

            items.append(
                CaseItem(
                    label=label,
                    statements=tuple(statements),
                )
            )

        node = CaseStatement(
            expression=" ".join(expression),
            items=tuple(items),
        )

        object.__setattr__(
            node,
            "location",
            token.source_location,
        )

        return node
