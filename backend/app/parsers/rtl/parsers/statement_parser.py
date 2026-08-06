"""
SystemVerilog procedural statement parser.
"""

from app.parsers.rtl.parser_context import ParserContext
from app.parsers.rtl.parsers.base_parser import BaseParser
from app.parsers.rtl.parsers.assignment_parser import AssignmentParser


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
        from app.parsers.rtl.parsers.begin_end_parser import BeginEndParser

        if IfParser.matches(context):
            return True

        if CaseParser.matches(context):
            return True

        if BeginEndParser.matches(context):
            return True

        if AssignmentParser.matches(context):
            return True

        return False

    @staticmethod
    def parse(
        context: ParserContext,
    ):

        from app.parsers.rtl.parsers.if_parser import IfParser
        from app.parsers.rtl.parsers.case_parser import CaseParser
        from app.parsers.rtl.parsers.begin_end_parser import BeginEndParser

        if IfParser.matches(context):
            return IfParser.parse(context)

        if CaseParser.matches(context):
            return CaseParser.parse(context)

        if BeginEndParser.matches(context):
            return BeginEndParser.parse(context)

        if AssignmentParser.matches(context):
            return AssignmentParser.parse(context)

        raise RuntimeError(
            "Unsupported procedural statement."
        )
