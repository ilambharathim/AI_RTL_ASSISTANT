"""
SystemVerilog procedural statement parser.
"""

from app.ast.procedural_assignment import ProceduralAssignment
from app.domain.rtl_tokens import RTLTokenType
from app.parsers.rtl.parser_context import ParserContext
from app.parsers.rtl.parsers.base_parser import BaseParser


class StatementParser(BaseParser):

    @staticmethod
    def matches(
        context: ParserContext,
    ) -> bool:

        if context.eof():
            return False

        #
        # Import lazily to avoid circular imports
        #
        from app.parsers.rtl.parsers.if_parser import IfParser
        from app.parsers.rtl.parsers.case_parser import CaseParser
        from app.parsers.rtl.parsers.begin_end_parser import (
            BeginEndParser,
        )

        if IfParser.matches(context):
            return True

        if CaseParser.matches(context):
            return True

        if BeginEndParser.matches(context):
            return True

        return (
            context.current().token_type
            == RTLTokenType.IDENTIFIER
        )

    @staticmethod
    def parse(
        context: ParserContext,
    ):

        from app.parsers.rtl.parsers.if_parser import IfParser
        from app.parsers.rtl.parsers.case_parser import CaseParser
        from app.parsers.rtl.parsers.begin_end_parser import (
            BeginEndParser,
        )

        if IfParser.matches(context):
            return IfParser.parse(context)

        if CaseParser.matches(context):
            return CaseParser.parse(context)

        if BeginEndParser.matches(context):
            return BeginEndParser.parse(context)

        #
        # Assignment
        #
        target = context.advance()

        operator = context.advance()

        expression = []

        while not context.eof():

            token = context.current()

            if (
                token.token_type == RTLTokenType.SYMBOL
                and token.value == ";"
            ):
                context.advance()
                break

            expression.append(token.value)

            context.advance()

        return ProceduralAssignment(
            target=target.value,
            operator=operator.value,
            expression=" ".join(expression),
        )
