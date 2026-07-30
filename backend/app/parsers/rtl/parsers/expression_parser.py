"""
SystemVerilog expression parser.

Current implementation:
- identifiers
- literals
- + - * /
with operator precedence.
"""

from app.ast.expression import (
    IdentifierExpression,
    LiteralExpression,
    BinaryExpression,
)

from app.domain.rtl_tokens import RTLTokenType

from app.parsers.rtl.parser_context import ParserContext
from app.parsers.rtl.parsers.base_parser import BaseParser


class ExpressionParser(BaseParser):

    #
    # Operator precedence
    #
    _PRECEDENCE = {
        "*": 20,
        "/": 20,
        "%": 20,
        "+": 10,
        "-": 10,
    }

    @staticmethod
    def parse(
        context: ParserContext,
    ):

        return ExpressionParser._parse_binary(
            context,
            0,
        )

    #
    # Pratt-style precedence climbing
    #
    @staticmethod
    def _parse_binary(
        context,
        min_precedence,
    ):

        left = ExpressionParser._parse_primary(
            context,
        )

        while not context.eof():

            token = context.current()

            if token.token_type != RTLTokenType.OPERATOR:
                break

            if token.value not in ExpressionParser._PRECEDENCE:
                break

            precedence = ExpressionParser._PRECEDENCE[
                token.value
            ]

            if precedence < min_precedence:
                break

            operator = token.value

            context.advance()

            right = ExpressionParser._parse_binary(
                context,
                precedence + 1,
            )

            left = BinaryExpression(
                operator=operator,
                left=left,
                right=right,
            )

        return left

    #
    # Primary expressions
    #
    @staticmethod
    def _parse_primary(
        context,
    ):

        if context.eof():
            raise RuntimeError(
                "Unexpected EOF while parsing expression."
            )

        token = context.current()

        #
        # Identifier
        #
        if token.token_type == RTLTokenType.IDENTIFIER:

            context.advance()

            return IdentifierExpression(
                token.value,
            )

        #
        # Literal
        #
        if token.token_type in {

            RTLTokenType.NUMBER,
            RTLTokenType.REAL_NUMBER,
            RTLTokenType.TIME_LITERAL,

        }:

            context.advance()

            return LiteralExpression(
                token.value,
            )

        raise RuntimeError(
            f"Unexpected token in expression: {token.value}"
        )
