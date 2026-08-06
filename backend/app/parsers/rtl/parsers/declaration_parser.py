"""
SystemVerilog declaration parser.
"""

from app.parsers.rtl.parsers.base_parser import BaseParser

from app.parsers.rtl.parsers.parameter_parser import ParameterParser
from app.parsers.rtl.parsers.signal_parser import SignalParser
from app.parsers.rtl.parsers.assign_parser import AssignParser
from app.parsers.rtl.parsers.always_parser import AlwaysParser
from app.parsers.rtl.parsers.module_instance_parser import ModuleInstanceParser


class DeclarationParser(BaseParser):

    @staticmethod
    def matches(context):

        return (

            ParameterParser.matches(context)

            or SignalParser.matches(context)

            or AssignParser.matches(context)

            or AlwaysParser.matches(context)

            or ModuleInstanceParser.matches(context)

        )

    @staticmethod
    def parse(context):

        if ParameterParser.matches(context):
            return ParameterParser.parse(context)

        if SignalParser.matches(context):
            return SignalParser.parse(context)

        if AssignParser.matches(context):
            return AssignParser.parse(context)

        if AlwaysParser.matches(context):
            return AlwaysParser.parse(context)

        if ModuleInstanceParser.matches(context):
            return ModuleInstanceParser.parse(context)

        raise RuntimeError(
            "Unsupported declaration."
        )

