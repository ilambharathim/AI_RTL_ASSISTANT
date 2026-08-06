"""
Named port connection parser.

Parses:

.port(signal)
"""

from app.ast.port_connection import PortConnection

from app.domain.rtl_tokens import RTLTokenType

from app.parsers.rtl.parsers.base_parser import BaseParser
from app.parsers.rtl.parsers.expression_parser import ExpressionParser


class PortConnectionParser(BaseParser):

    @staticmethod
    def parse(context):

        #
        # .
        #
        if context.current().value != ".":

            raise RuntimeError(
                "Expected '.'."
            )

        context.advance()

        #
        # Port name
        #
        if context.current().token_type != RTLTokenType.IDENTIFIER:

            raise RuntimeError(
                "Expected port name."
            )

        port_name = context.advance().value

        #
        # (
        #
        if context.current().value != "(":

            raise RuntimeError(
                "Expected '('."
            )

        context.advance()

        expression = ExpressionParser.parse(
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

        node = PortConnection(

            port_name,

            expression,

        )

        object.__setattr__(
            node,
            "location",
            token.source_location,
        )

        return node

