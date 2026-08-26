"""
SystemVerilog procedural assignment parser.

Supports:

    q <= d;
    q = d;
    q <= a + b;
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

        if context.current().token_type != RTLTokenType.IDENTIFIER:
            return False

        if context.index + 1 >= len(context.tokens):
            return False

        operator = context.tokens[context.index + 1]

        return (
            operator.token_type == RTLTokenType.OPERATOR
            and operator.value in {"=", "<="}
        )

    @staticmethod
    def parse(
        context: ParserContext,
    ) -> ProceduralAssignment:

        target = context.advance()

        operator = context.advance()

        expression = ExpressionParser.parse(
            context,
        )

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
            target.source_location,
        )

        return node
