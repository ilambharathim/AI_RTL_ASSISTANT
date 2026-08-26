"""
SystemVerilog expression parser.

Supports

- literals
- identifiers
- function calls
- unary operators
- binary operators
- parentheses
"""

from app.ast.expression import (
    IdentifierExpression,
    LiteralExpression,
    UnaryExpression,
    BinaryExpression,
    FunctionCallExpression,
)

from app.domain.rtl_tokens import RTLTokenType

from app.parsers.rtl.parser_context import ParserContext
from app.parsers.rtl.parsers.base_parser import BaseParser


class ExpressionParser(BaseParser):

    _PRECEDENCE = {

        "*":110,
        "/":110,
        "%":110,

        "+":100,
        "-":100,

        "<<":90,
        ">>":90,
        "<<<":90,
        ">>>":90,

        "<":80,
        "<=":80,
        ">":80,
        ">=":80,

        "==":70,
        "!=":70,
        "===":70,
        "!==":70,

        "&":60,

        "^":50,
        "^~":50,
        "~^":50,

        "|":40,

        "&&":30,

        "||":20,
    }

    _UNARY = {

        "+",
        "-",
        "!",
        "~",
        "&",
        "|",
        "^",

    }

    @staticmethod
    def parse(
        context,
    ):

        return ExpressionParser._binary(
            context,
            0,
        )

    @staticmethod
    def _binary(
        context,
        minimum,
    ):

        left = ExpressionParser._primary(
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

            if precedence < minimum:
                break

            operator = token.value

            context.advance()

            right = ExpressionParser._binary(
                context,
                precedence + 1,
            )

            left = BinaryExpression(
                operator=operator,
                left=left,
                right=right,
            )

            object.__setattr__(
                left,
                "location",
                token.source_location,
            )

        return left

    @staticmethod
    def _parse_arguments(
        context,
    ):

        arguments = []

        #
        # (
        #
        context.advance()

        while not context.eof():

            if (
                context.current().token_type == RTLTokenType.SYMBOL
                and context.current().value == ")"
            ):

                context.advance()

                break

            arguments.append(

                ExpressionParser.parse(
                    context,
                )

            )

            if (
                context.current().token_type == RTLTokenType.SYMBOL
                and context.current().value == ","
            ):

                context.advance()

                continue

            if (
                context.current().token_type == RTLTokenType.SYMBOL
                and context.current().value == ")"
            ):

                context.advance()

                break

        return tuple(arguments)

    @staticmethod
    def _primary(
        context,
    ):

        if context.eof():

            raise RuntimeError(
                "Unexpected EOF."
            )

        token = context.current()

        #
        # unary
        #
        if (
            token.token_type == RTLTokenType.OPERATOR
            and token.value in ExpressionParser._UNARY
        ):

            operator = token.value

            context.advance()

            return UnaryExpression(

                operator,

                ExpressionParser._primary(
                    context,
                ),

            )

        #
        # (
        #
        if (
            token.token_type == RTLTokenType.SYMBOL
            and token.value == "("
        ):

            context.advance()

            expression = ExpressionParser.parse(
                context,
            )

            if (
                context.eof()
                or context.current().value != ")"
            ):

                raise RuntimeError(
                    "Expected ')'"
                )

            context.advance()

            return expression

        #
        # identifier / function call
        #
        if token.token_type in {

            RTLTokenType.IDENTIFIER,
            RTLTokenType.SYSTEM_IDENTIFIER,

        }:

            name = token.value

            context.advance()

            if (

                not context.eof()

                and context.current().token_type == RTLTokenType.SYMBOL

                and context.current().value == "("

            ):

                return FunctionCallExpression(

                    function_name=name,

                    arguments=ExpressionParser._parse_arguments(
                        context,
                    ),

                )

            node = IdentifierExpression(
                name,
            )
            object.__setattr__(
                node,
                "location",
                token.source_location,
            )
            return node

        #
        # literal
        #
        if token.token_type in {

            RTLTokenType.NUMBER,
            RTLTokenType.REAL_NUMBER,
            RTLTokenType.TIME_LITERAL,

        }:

            context.advance()

            node = LiteralExpression(
                token.value,
            )

            object.__setattr__(
                node,
                "location",
                token.source_location,
            )

            return node

        raise RuntimeError(

            f"Unexpected token '{token.value}'"

        )
