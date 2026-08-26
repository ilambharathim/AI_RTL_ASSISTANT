"""
SystemVerilog always block parser.
"""

from app.ast.always_block import AlwaysBlock
from app.domain.rtl_tokens import RTLTokenType
from app.parsers.rtl.parser_context import ParserContext
from app.parsers.rtl.parsers.base_parser import BaseParser
from app.parsers.rtl.parsers.statement_parser import StatementParser


class AlwaysParser(BaseParser):

    _BLOCK_TYPES = {
        "always",
        "always_comb",
        "always_ff",
        "always_latch",
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
            and token.value in AlwaysParser._BLOCK_TYPES
        )

    @staticmethod
    def parse(
        context: ParserContext,
    ) -> AlwaysBlock:

        #
        # Lazy import to avoid circular dependency
        #
        from app.parsers.rtl.parsers.declaration_parser import (
            DeclarationParser,
        )

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

            context.advance()

            sensitivity_tokens = []

            #
            # Collect everything inside @( ... )
            #
            while not context.eof():

                token = context.current()

                if (
                    token.token_type == RTLTokenType.SYMBOL
                    and token.value == ")"
                ):
                    context.advance()
                    break

                sensitivity_tokens.append(token.value)
                context.advance()

            sensitivity = "@(" + " ".join(
                sensitivity_tokens
            ) + ")"

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
            # End of block
            #
            if (
                token.token_type == RTLTokenType.KEYWORD
                and token.value == "end"
            ):

                context.advance()
                break

            if DeclarationParser.matches(
                context,
            ):

                statements.append(
                    DeclarationParser.parse(
                        context,
                    )
                )

                continue

            if StatementParser.matches(
                context,
            ):

                statements.append(
                    StatementParser.parse(
                        context,
                    )
                )

                continue

            context.advance()

        node = AlwaysBlock(

            block_type=block_type,

            sensitivity=sensitivity,

            statements=tuple(
                statements,
            ),

        )

        object.__setattr__(
            node,
            "location",
            token.source_location,
        )

        return node
