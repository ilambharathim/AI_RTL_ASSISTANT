"""
Compilation Unit parser.
"""

from app.ast.compilation_unit import CompilationUnit
from app.parsers.rtl.parser_context import ParserContext
from app.parsers.rtl.parsers.base_parser import BaseParser
from app.parsers.rtl.parsers.module_parser import ModuleParser


class CompilationUnitParser(BaseParser):

    @staticmethod
    def matches(
        context: ParserContext,
    ) -> bool:

        return True

    @staticmethod
    def parse(
        context: ParserContext,
    ) -> CompilationUnit:

        declarations = []

        token = None

        if not context.eof():
            token = context.current()

        while not context.eof():

            if ModuleParser.matches(context):

                declarations.append(
                    ModuleParser.parse(context)
                )

                continue

            context.advance()

        node = CompilationUnit(
            declarations=tuple(declarations),
        )

        if token is not None:
            object.__setattr__(
                node,
                "location",
                token.source_location,
            )

        return node
