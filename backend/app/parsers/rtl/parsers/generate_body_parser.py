"""
SystemVerilog generate-body parser.

Parses the contents of:

begin
...
end

or:

begin : generate_name
...
end
"""

from app.domain.rtl_tokens import RTLTokenType

from app.parsers.rtl.parsers.base_parser import BaseParser
from app.parsers.rtl.parsers.module_instance_parser import (
    ModuleInstanceParser,
)


class GenerateBodyParser(BaseParser):

    @staticmethod
    def parse(context):

        members = []

        #
        # begin
        #
        if (
            context.eof()
            or context.current().token_type
            != RTLTokenType.KEYWORD
            or context.current().value != "begin"
        ):
            raise RuntimeError(
                "Expected 'begin' for generate body."
            )

        context.advance()

        #
        # Optional generate block label:
        #
        # begin : gen_loop
        #
        if (
            not context.eof()
            and context.current().value == ":"
        ):
            context.advance()

            if (
                context.eof()
                or context.current().token_type
                != RTLTokenType.IDENTIFIER
            ):
                raise RuntimeError(
                    "Expected generate block label."
                )

            context.advance()

        #
        # Import nested generate parsers lazily.
        #
        # GenerateIfParser and GenerateForParser both import
        # GenerateBodyParser, so importing them at module scope
        # would create a circular import.
        #
        from app.parsers.rtl.parsers.generate_if_parser import (
            GenerateIfParser,
        )

        from app.parsers.rtl.parsers.generate_for_parser import (
            GenerateForParser,
        )

        #
        # Parse declarations/members until end.
        #
        while not context.eof():

            #
            # end
            #
            if (
                context.current().token_type
                == RTLTokenType.KEYWORD
                and context.current().value == "end"
            ):
                context.advance()
                break

            #
            # Nested generate-if
            #
            if GenerateIfParser.matches(context):
                members.append(
                    GenerateIfParser.parse(
                        context,
                    )
                )
                continue

            #
            # Nested generate-for
            #
            if GenerateForParser.matches(context):
                members.append(
                    GenerateForParser.parse(
                        context,
                    )
                )
                continue

            #
            # Module instance
            #
            if ModuleInstanceParser.matches(context):
                members.append(
                    ModuleInstanceParser.parse(
                        context,
                    )
                )
                continue

            #
            # Unsupported generate-body construct.
            #
            context.advance()

        return tuple(members)
