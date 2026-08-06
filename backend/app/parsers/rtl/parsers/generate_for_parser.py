"""
SystemVerilog generate-for parser.

Parses:

for(genvar i=0; i<N; i=i+1)
    ...
"""

from app.ast import GenerateFor

from app.domain.rtl_tokens.token_type import RTLTokenType

from app.parsers.rtl.parsers.base_parser import BaseParser
from app.parsers.rtl.parsers.expression_parser import ExpressionParser
from app.parsers.rtl.parsers.module_instance_parser import (
    ModuleInstanceParser,
)


class GenerateForParser(BaseParser):

    @staticmethod
    def matches(
        context,
    ):

        if context.eof():
            return False

        return (
            context.current().token_type
            == RTLTokenType.KEYWORD
            and context.current().value == "for"
        )

    @staticmethod
    def parse(
        context,
    ):

        token = context.current()

        #
        # for
        #
        context.advance()

        #
        # (
        #
        if (
            context.eof()
            or context.current().value != "("
        ):
            raise RuntimeError(
                "Expected '(' after for."
            )

        context.advance()

        #
        # Optional genvar
        #
        if (
            not context.eof()
            and context.current().token_type
            == RTLTokenType.KEYWORD
            and context.current().value == "genvar"
        ):
            context.advance()

        #
        # Variable
        #
        if (
            context.eof()
            or context.current().token_type
            != RTLTokenType.IDENTIFIER
        ):
            raise RuntimeError(
                "Expected loop variable."
            )

        variable = context.advance().value

        #
        # =
        #
        if context.current().value != "=":
            raise RuntimeError(
                "Expected '='."
            )

        context.advance()

        initializer = ExpressionParser.parse(
            context,
        )

        #
        # ;
        #
        if context.current().value != ";":
            raise RuntimeError(
                "Expected ';'."
            )

        context.advance()

        #
        # Condition
        #
        condition = ExpressionParser.parse(
            context,
        )

        #
        # ;
        #
        if context.current().value != ";":
            raise RuntimeError(
                "Expected ';'."
            )

        context.advance()

        #
        # Update
        #
        update = ExpressionParser.parse(
            context,
        )

        #
        # )
        #
        if context.current().value != ")":
            raise RuntimeError(
                "Expected ')'."
            )

        context.advance()

        members = []

        if ModuleInstanceParser.matches(
            context,
        ):

            members.append(
                ModuleInstanceParser.parse(
                    context,
                )
            )

        node = GenerateFor(

            variable=variable,

            initializer=initializer,

            condition=condition,

            update=update,

            members=tuple(
                members,
            ),

        )

        object.__setattr__(
            node,
            "location",
            token.source_location,
        )

        return node

