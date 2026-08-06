"""
SystemVerilog procedural assignment parser.
"""

from app.ast.procedural_assignment import ProceduralAssignment

from app.domain.rtl_tokens import RTLTokenType

from app.parsers.rtl.parser_context import ParserContext

from app.parsers.rtl.parsers.base_parser import BaseParser
from app.parsers.rtl.parsers.expression_parser import ExpressionParser


class AssignmentParser(BaseParser):

    @staticmethod
    def matches(
        context: ParserContext,
    ) -> bool:

        if context.eof():
            return False

        return (
            context.current().token_type
            == RTLTokenType.IDENTIFIER
        )

    @staticmethod
    def parse(
        context: ParserContext,
    ) -> ProceduralAssignment:

        #
        # target
        #
        target = context.advance()

        token = target

        #
        # assignment operator
        #
        operator = context.advance()

        #
        # Parse Expression AST
        #
        expression = ExpressionParser.parse(
            context,
        )

        #
        # Consume ';'
        #
        if (
            not context.eof()
            and context.current().token_type == RTLTokenType.SYMBOL
            and context.current().value == ";"
        ):
            context.advance()

        node = ProceduralAssignment(
            target=target.value,
            operator=operator.value,
            expression=expression,
        )

        object.__setattr__(
            node,
            "location",
            token.source_location,
        )

        return node
