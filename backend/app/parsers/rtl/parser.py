"""
Deterministic RTL parser.
"""

from app.parsers.rtl.parser_context import ParserContext
from app.parsers.rtl.parser_registry import PARSERS
from app.parsers.rtl.parser_result import RTLParserResult


class RTLParser:

    def parse(
        self,
        tokens,
    ) -> RTLParserResult:

        context = ParserContext(tokens)

        diagnostics = []

        syntax_tree = None

        for parser in PARSERS:

            if parser.matches(context):

                syntax_tree = parser.parse(context)

                break

        return RTLParserResult(
            syntax_tree=syntax_tree,
            diagnostics=tuple(diagnostics),
        )
