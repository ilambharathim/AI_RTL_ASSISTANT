"""
SystemVerilog module parser.
"""

from app.ast.module_declaration import ModuleDeclaration
from app.ast.port_declaration import PortDeclaration
from app.domain.rtl_tokens import RTLTokenType
from app.parsers.rtl.parser_context import ParserContext
from app.parsers.rtl.parsers.base_parser import BaseParser
from app.parsers.rtl.parsers.declaration_parser import DeclarationParser
from app.parsers.rtl.parsers.assign_parser import AssignParser
from app.parsers.rtl.parsers.always_parser import AlwaysParser


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

        context.advance()

        module_name = context.advance()

        ports = []

        if (
            not context.eof()
            and context.current().token_type == RTLTokenType.SYMBOL
            and context.current().value == "("
        ):

            context.advance()

            while not context.eof():

                token = context.current()

                if (
                    token.token_type == RTLTokenType.SYMBOL
                    and token.value == ")"
                ):
                    context.advance()
                    break

                if token.token_type == RTLTokenType.IDENTIFIER:

                    ports.append(
                        PortDeclaration(
                            name=token.value,
                        )
                    )

                context.advance()

        members = []

        while not context.eof():

            token = context.current()

            if (
                token.token_type == RTLTokenType.KEYWORD
                and token.value == "endmodule"
            ):
                context.advance()
                break

            #
            # All declarations are owned by DeclarationParser
            #
            if DeclarationParser.matches(context):

                members.append(
                    DeclarationParser.parse(context)
                )

                continue

            if AssignParser.matches(context):

                members.append(
                    AssignParser.parse(context)
                )

                continue

            if AlwaysParser.matches(context):

                members.append(
                    AlwaysParser.parse(context)
                )

                continue

            context.advance()

        node = ModuleDeclaration(
            name=module_name.value,
            ports=tuple(ports),
            members=tuple(members),
        )

        object.__setattr__(
            node,
            "location",
            token.source_location,
        )

        return node
