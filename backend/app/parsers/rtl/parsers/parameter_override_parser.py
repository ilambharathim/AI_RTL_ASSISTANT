"""
SystemVerilog parameter override parser.

Parses:

.WIDTH(32)

.DEPTH(SIZE+1)
"""

from app.ast.parameter_override import ParameterOverride

from app.domain.rtl_tokens import RTLTokenType

from app.parsers.rtl.parsers.base_parser import BaseParser
from app.parsers.rtl.parsers.expression_parser import ExpressionParser


class ParameterOverrideParser(BaseParser):

    @staticmethod
    def parse(
        context,
    ):

        token = context.current()

        #
        # .
        #
        if (
            context.eof()
            or context.current().value != "."
        ):
            raise RuntimeError(
                "Expected '.'."
            )

        context.advance()

        #
        # parameter name
        #
        if (
            context.eof()
            or context.current().token_type
            != RTLTokenType.IDENTIFIER
        ):
            raise RuntimeError(
                "Expected parameter name."
            )

        name = context.advance().value

        #
        # (
        #
        if (
            context.eof()
            or context.current().value != "("
        ):
            raise RuntimeError(
                "Expected '('."
            )

        context.advance()

        #
        # expression
        #
        expression = ExpressionParser.parse(
            context,
        )

        #
        # )
        #
        if (
            context.eof()
            or context.current().value != ")"
        ):
            raise RuntimeError(
                "Expected ')'."
            )

        context.advance()

        node = ParameterOverride(

            name=name,

            expression=expression,

        )

        object.__setattr__(
            node,
            "location",
            token.source_location,
        )

        return node

