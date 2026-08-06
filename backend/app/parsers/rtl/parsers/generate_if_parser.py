"""
SystemVerilog generate-if parser.

Parses:

if (<expression>)
    ...
else
    ...
"""

from app.ast import GenerateIf

from app.domain.rtl_tokens.token_type import RTLTokenType

from app.parsers.rtl.parsers.base_parser import BaseParser
from app.parsers.rtl.parsers.expression_parser import ExpressionParser
from app.parsers.rtl.parsers.module_instance_parser import ModuleInstanceParser


class GenerateIfParser(BaseParser):

    @staticmethod
    def matches(
        context,
    ):

        if context.eof():
            return False

        return (
            context.current().token_type
            == RTLTokenType.KEYWORD
            and context.current().value == "if"
        )

    @staticmethod
    def parse(
        context,
    ):

        token = context.current()

        #
        # if
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
                "Expected '(' after if."
            )

        context.advance()

        #
        # condition
        #
        condition = ExpressionParser.parse(
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

        #
        # True branch
        #
        true_members = []

        if ModuleInstanceParser.matches(
            context,
        ):

            true_members.append(
                ModuleInstanceParser.parse(
                    context,
                )
            )

        #
        # Optional else
        #
        false_members = []

        if (
            not context.eof()
            and context.current().token_type
            == RTLTokenType.KEYWORD
            and context.current().value == "else"
        ):

            context.advance()

            if ModuleInstanceParser.matches(
                context,
            ):

                false_members.append(
                    ModuleInstanceParser.parse(
                        context,
                    )
                )

        node = GenerateIf(

            condition=condition,

            true_members=tuple(
                true_members,
            ),

            false_members=tuple(
                false_members,
            ),

        )

        object.__setattr__(
            node,
            "location",
            token.source_location,
        )

        return node

