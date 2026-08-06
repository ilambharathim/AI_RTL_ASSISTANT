"""
SystemVerilog generate parser.

Dispatches generate constructs.
"""

from app.domain.rtl_tokens.token_type import RTLTokenType

from app.parsers.rtl.parsers.base_parser import BaseParser

from app.parsers.rtl.parsers.generate_if_parser import (
    GenerateIfParser,
)

from app.parsers.rtl.parsers.generate_for_parser import (
    GenerateForParser,
)


class GenerateParser(BaseParser):

    @staticmethod
    def matches(
        context,
    ):

        if context.eof():
            return False

        return (
            context.current().token_type
            == RTLTokenType.KEYWORD
            and context.current().value
            == "generate"
        )

    @staticmethod
    def parse(
        context,
    ):

        token = context.current()

        #
        # generate
        #
        context.advance()

        members = []

        while not context.eof():

            if (
                context.current().token_type
                == RTLTokenType.KEYWORD
                and context.current().value
                == "endgenerate"
            ):
                break

            if GenerateIfParser.matches(
                context,
            ):

                members.append(
                    GenerateIfParser.parse(
                        context,
                    )
                )

                continue

            if GenerateForParser.matches(
                context,
            ):

                members.append(
                    GenerateForParser.parse(
                        context,
                    )
                )

                continue

            raise RuntimeError(
                "Unsupported generate construct."
            )

        #
        # endgenerate
        #
        if (
            context.eof()
            or context.current().value
            != "endgenerate"
        ):
            raise RuntimeError(
                "Expected 'endgenerate'."
            )

        context.advance()

        from app.ast import GenerateBlock

        node = GenerateBlock(
            tuple(
                members,
            )
        )

        object.__setattr__(
            node,
            "location",
            token.source_location,
        )

        return node

