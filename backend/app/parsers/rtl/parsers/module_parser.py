"""
SystemVerilog module parser.

Compatibility-first parser:
the parser still produces the legacy AST consumed by
the current semantic/elaboration pipeline.
"""

from app.ast.module_declaration import ModuleDeclaration

from app.domain.rtl_tokens import RTLTokenType

from app.parsers.rtl.parser_context import ParserContext

from app.parsers.rtl.parsers.base_parser import BaseParser
from app.parsers.rtl.parsers.declaration_parser import DeclarationParser
from app.parsers.rtl.parsers.assign_parser import AssignParser
from app.parsers.rtl.parsers.always_parser import AlwaysParser
from app.parsers.rtl.parsers.port_parser import PortParser
from app.parsers.rtl.parsers.generate_parser import GenerateParser
from app.parsers.rtl.parsers.module_instance_parser import ModuleInstanceParser


class ModuleParser(BaseParser):

    @staticmethod
    def matches(context: ParserContext) -> bool:

        if context.eof():
            return False

        token = context.current()

        return (
            token.token_type == RTLTokenType.KEYWORD
            and token.value == "module"
        )

    @staticmethod
    def parse(context: ParserContext) -> ModuleDeclaration:

        module_token = context.advance()

        module_name = context.advance()

        ports = []

        #
        # Module port list.
        #
        if (
            not context.eof()
            and context.current().token_type == RTLTokenType.SYMBOL
            and context.current().value == "("
        ):

            context.advance()

            while not context.eof():

                if (
                    context.current().token_type == RTLTokenType.SYMBOL
                    and context.current().value == ")"
                ):
                    context.advance()
                    break

                if PortParser.matches(context):

                    ports.append(
                        PortParser.parse(context)
                    )

                    if (
                        not context.eof()
                        and context.current().token_type == RTLTokenType.SYMBOL
                        and context.current().value == ","
                    ):
                        context.advance()

                    continue

                context.advance()

        #
        # Module members.
        #
        members = []

        while not context.eof():

            token = context.current()

            #
            # End module.
            #
            if (
                token.token_type == RTLTokenType.KEYWORD
                and token.value == "endmodule"
            ):
                context.advance()
                break

            #
            # Generate constructs.
            #
            if GenerateParser.matches(context):

                generated = GenerateParser.parse(context)

                if generated is not None:
                    members.append(generated)

                continue

            #
            # Declarations.
            #
            if DeclarationParser.matches(context):

                members.append(
                    DeclarationParser.parse(context)
                )

                continue

            #
            # Continuous assignments.
            #
            if AssignParser.matches(context):

                members.append(
                    AssignParser.parse(context)
                )

                continue

            #
            # Always blocks.
            #
            if AlwaysParser.matches(context):

                members.append(
                    AlwaysParser.parse(context)
                )

                continue

            #
            # Module instances.
            #
            if ModuleInstanceParser.matches(context):

                members.append(
                    ModuleInstanceParser.parse(context)
                )

                continue

            #
            # Unknown token.
            #
            context.advance()

        node = ModuleDeclaration(
            name=module_name.value,
            ports=tuple(ports),
            members=tuple(members),
        )

        object.__setattr__(
            node,
            "location",
            module_token.source_location,
        )

        return node
