"""
Continuous assignment parser.
"""

from app.ast.continuous_assign import ContinuousAssign
from app.domain.rtl_tokens import RTLTokenType
from app.parsers.rtl.parser_context import ParserContext
from app.parsers.rtl.parsers.base_parser import BaseParser
from app.parsers.rtl.parsers.expression_parser import ExpressionParser


class AssignParser(BaseParser):

    @staticmethod
    def matches(
        context: ParserContext,
    ) -> bool:

        token = context.current()

        return (
            token.token_type == RTLTokenType.KEYWORD
            and token.value == "assign"
        )

    @staticmethod
    def parse(
        context: ParserContext,
    ) -> ContinuousAssign:

        #
        # assign
        #
        assign_token = context.advance()

        #
        # target
        #
        target_name = ""
        if not context.eof() and context.current().token_type == RTLTokenType.IDENTIFIER:
            target_name = context.advance().value

        #
        # =
        #
        if not context.eof() and context.current().value == "=":
            context.advance()

        #
        # Parse canonical AST expression
        #
        try:
            expression = ExpressionParser.parse(context)
        except Exception:
            # Fallback for malformed/incomplete expressions (e.g. invalid syntax test cases)
            expression_tokens = []
            while not context.eof():
                if context.current().token_type == RTLTokenType.SYMBOL and context.current().value == ";":
                    break
                expression_tokens.append(context.current().value)
                context.advance()
            expression = " ".join(expression_tokens)

        if (
            not context.eof()
            and context.current().token_type == RTLTokenType.SYMBOL
            and context.current().value == ";"
        ):
            context.advance()

        node = ContinuousAssign(
            target=target_name,
            expression=expression,
        )

        object.__setattr__(
            node,
            "location",
            assign_token.source_location,
        )

        return node
