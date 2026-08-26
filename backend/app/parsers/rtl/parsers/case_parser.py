"""
SystemVerilog case statement parser.

Supports:

    case (...)
    casez (...)
    casex (...)

including:

    label: statement;
    label: begin ... end
    default: statement;
"""

from app.ast.case_statement import CaseItem, CaseStatement
from app.domain.rtl_tokens import RTLTokenType
from app.parsers.rtl.parser_context import ParserContext
from app.parsers.rtl.parsers.base_parser import BaseParser


class CaseParser(BaseParser):

    _CASE_KEYWORDS = {
        "case",
        "casez",
        "casex",
    }

    @staticmethod
    def matches(
        context: ParserContext,
    ) -> bool:

        if context.eof():
            return False

        token = context.current()

        return (
            token.token_type == RTLTokenType.KEYWORD
            and token.value in CaseParser._CASE_KEYWORDS
        )

    @staticmethod
    def parse(
        context: ParserContext,
    ) -> CaseStatement:

        from app.parsers.rtl.parsers.statement_parser import (
            StatementParser,
        )

        #
        # case / casez / casex
        #
        case_token = context.advance()

        #
        # (
        #
        if (
            context.eof()
            or context.current().token_type != RTLTokenType.SYMBOL
            or context.current().value != "("
        ):
            raise RuntimeError(
                f"Expected '(' after '{case_token.value}'."
            )

        context.advance()

        #
        # Case expression
        #
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

        #
        # Case items
        #
        items = []

        while not context.eof():

            token = context.current()

            #
            # endcase
            #
            if (
                token.token_type == RTLTokenType.KEYWORD
                and token.value == "endcase"
            ):
                context.advance()
                break

            #
            # Read label until ':'
            #
            label = []

            while not context.eof():

                token = context.current()

                if (
                    token.token_type == RTLTokenType.SYMBOL
                    and token.value == ":"
                ):
                    context.advance()
                    break

                #
                # A malformed case item should not consume
                # the entire remainder of the block.
                #
                if (
                    token.token_type == RTLTokenType.KEYWORD
                    and token.value == "endcase"
                ):
                    break

                label.append(token.value)
                context.advance()

            #
            # Parse the statement belonging to this case item.
            #
            statements = []

            if (
                not context.eof()
                and StatementParser.matches(context)
            ):
                statements.append(
                    StatementParser.parse(context)
                )

            #
            # If no statement was parsed, avoid an infinite loop.
            #
            if not statements and not context.eof():
                context.advance()

            items.append(
                CaseItem(
                    label=" ".join(label),
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
            case_token.source_location,
        )

        return node
