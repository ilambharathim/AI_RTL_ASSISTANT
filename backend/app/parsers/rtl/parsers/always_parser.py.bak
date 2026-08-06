"""
SystemVerilog always block parser.
"""

from app.ast.always_block import AlwaysBlock
from app.domain.rtl_tokens import RTLTokenType
from app.parsers.rtl.parser_context import ParserContext
from app.parsers.rtl.parsers.base_parser import BaseParser

from app.parsers.rtl.parsers.signal_parser import SignalParser
from app.parsers.rtl.parsers.statement_parser import StatementParser
from app.parsers.rtl.parsers.if_parser import IfParser
from app.parsers.rtl.parsers.case_parser import CaseParser


class AlwaysParser(BaseParser):

    _BLOCK_TYPES = {
        "always",
        "always_comb",
        "always_ff",
        "always_latch",
    }

    @staticmethod
    def matches(context):

        if context.eof():
            return False

        token = context.current()

        return (
            token.token_type == RTLTokenType.KEYWORD
            and token.value in AlwaysParser._BLOCK_TYPES
        )

    @staticmethod
    def parse(context):

        block_type = context.advance().value

        sensitivity = ""

        #
        # Parse @(...)
        #
        if (
            not context.eof()
            and context.current().token_type == RTLTokenType.OPERATOR
            and context.current().value == "@"
        ):

            sensitivity = "@"

            context.advance()

            while not context.eof():

                token = context.current()

                sensitivity += token.value

                context.advance()

                if (
                    token.token_type == RTLTokenType.SYMBOL
                    and token.value == ")"
                ):
                    break

        #
        # Find begin
        #
        while not context.eof():

            token = context.current()

            if (
                token.token_type == RTLTokenType.KEYWORD
                and token.value == "begin"
            ):
                context.advance()
                break

            context.advance()

        statements = []

        while not context.eof():

            token = context.current()

            #
            # end
            #
            if (
                token.token_type == RTLTokenType.KEYWORD
                and token.value == "end"
            ):
                context.advance()
                break

            #
            # NEW:
            # procedural declarations
            #
            if SignalParser.matches(context):

                statements.append(
                    SignalParser.parse(context)
                )

                continue

            #
            # if
            #
            if IfParser.matches(context):

                statements.append(
                    IfParser.parse(context)
                )

                continue

            #
            # case
            #
            if CaseParser.matches(context):

                statements.append(
                    CaseParser.parse(context)
                )

                continue

            #
            # assignment
            #
            if StatementParser.matches(context):

                statements.append(
                    StatementParser.parse(context)
                )

                continue

            context.advance()

        return AlwaysBlock(
            block_type=block_type,
            sensitivity=sensitivity,
            statements=tuple(statements),
        )
