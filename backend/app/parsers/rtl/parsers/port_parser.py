"""
SystemVerilog port parser.

Supports:

input logic clk
output logic [7:0] data
"""

from app.ast.port_declaration import PortDeclaration

from app.domain.rtl_tokens import RTLTokenType

from app.parsers.rtl.parsers.base_parser import BaseParser
from app.parsers.rtl.parsers.packed_range_parser import PackedRangeParser


class PortParser(BaseParser):

    _DIRECTIONS = {

        "input",

        "output",

        "inout",

    }

    _TYPES = {

        "logic",

        "wire",

        "reg",

        "bit",

    }

    @staticmethod
    def matches(context):

        if context.eof():

            return False

        token = context.current()

        return (

            token.token_type == RTLTokenType.KEYWORD

            and token.value in PortParser._DIRECTIONS

        )

    @staticmethod
    def parse(context):

        #
        # direction
        #
        direction = context.advance().value

        #
        # optional type
        #
        signal_type = "logic"

        if (

            not context.eof()

            and context.current().value in PortParser._TYPES

        ):

            signal_type = context.advance().value

        #
        # optional packed range
        #
        packed_range = None

        if PackedRangeParser.matches(

            context,

        ):

            packed_range = PackedRangeParser.parse(

                context,

            )

        #
        # identifier
        #
        if (

            context.eof()

            or context.current().token_type

            != RTLTokenType.IDENTIFIER

        ):

            raise RuntimeError(

                "Expected port identifier."

            )

        name = context.advance().value

        node = PortDeclaration(

            direction=direction,

            signal_type=signal_type,

            packed_range=packed_range,

            name=name,

        )

        object.__setattr__(
            node,
            "location",
            token.source_location,
        )

        return node

