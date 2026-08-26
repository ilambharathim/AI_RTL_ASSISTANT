"""
Deterministic RTL parser.

The parser currently produces the legacy RTL AST and also exposes
the migrated domain RTL AST through the adapter.
"""

from app.parsers.rtl.parser_context import ParserContext
from app.parsers.rtl.parser_registry import PARSERS
from app.parsers.rtl.parser_result import RTLParserResult
from app.parsers.rtl.adapters import LegacyToRTLASTAdapter


class RTLParser:
    """
    Deterministic RTL parser entry point.
    """

    def parse(
        self,
        tokens,
    ) -> RTLParserResult:
        """
        Parse an RTL token stream.

        The selected parser produces the legacy AST consumed by
        the current semantic and elaboration pipeline.

        The legacy AST is additionally converted into the new
        domain RTL AST.
        """

        context = ParserContext(tokens)

        diagnostics = []

        syntax_tree = None

        for parser in PARSERS:

            if parser.matches(context):

                syntax_tree = parser.parse(
                    context,
                )

                break

        rtl_ast = None

        if syntax_tree is not None:

            rtl_ast = LegacyToRTLASTAdapter.convert(
                syntax_tree,
            )

        return RTLParserResult(
            syntax_tree=syntax_tree,
            rtl_ast=rtl_ast,
            diagnostics=tuple(diagnostics),
        )
