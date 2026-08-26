"""
SystemVerilog generate construct dispatcher.

Dispatches:

generate
    if (...)
        ...
endgenerate

and generate-for constructs.
"""

from app.domain.rtl_tokens import RTLTokenType
from app.parsers.rtl.parsers.base_parser import BaseParser
from app.parsers.rtl.parsers.generate_if_parser import GenerateIfParser
from app.parsers.rtl.parsers.generate_for_parser import GenerateForParser


class GenerateParser(BaseParser):

    @staticmethod
    def matches(context) -> bool:

        if context.eof():
            return False

        token = context.current()

        #
        # Explicit generate keyword.
        #
        if (
            token.token_type == RTLTokenType.KEYWORD
            and token.value == "generate"
        ):
            return True

        #
        # Some SystemVerilog forms may omit the explicit
        # generate/endgenerate wrapper.
        #
        if GenerateIfParser.matches(context):
            return True

        if GenerateForParser.matches(context):
            return True

        return False

    @staticmethod
    def parse(context):

        #
        # Optional explicit "generate" wrapper.
        #
        explicit_generate = False

        if (
            not context.eof()
            and context.current().token_type == RTLTokenType.KEYWORD
            and context.current().value == "generate"
        ):
            explicit_generate = True
            context.advance()

        #
        # Parse the construct inside generate.
        #
        if GenerateIfParser.matches(context):

            node = GenerateIfParser.parse(context)

        elif GenerateForParser.matches(context):

            node = GenerateForParser.parse(context)

        else:

            #
            # Unknown/empty generate construct.
            #
            while (
                not context.eof()
                and not (
                    context.current().token_type
                    == RTLTokenType.KEYWORD
                    and context.current().value == "endgenerate"
                )
            ):
                context.advance()

            node = None

        #
        # Consume optional endgenerate.
        #
        if (
            explicit_generate
            and not context.eof()
            and context.current().token_type == RTLTokenType.KEYWORD
            and context.current().value == "endgenerate"
        ):
            context.advance()

        return node
