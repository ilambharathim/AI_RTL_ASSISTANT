"""
SystemVerilog port parser.

Supports examples such as:

input logic clk
output logic [7:0] data
inout wire [3:0] bus
input logic signed [7:0] addr
output logic unsigned [15:0] result
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
        "int",
        "integer",
    }

    _SIGNEDNESS = {
        "signed",
        "unsigned",
    }

    @staticmethod
    def matches(context) -> bool:
        if context.eof():
            return False

        token = context.current()

        return (
            token.token_type == RTLTokenType.KEYWORD
            and token.value in PortParser._DIRECTIONS
        )

    @staticmethod
    def parse(context):
        # Capture the starting token before advancing.
        start_token = context.current()

        # direction
        direction = context.advance().value

        # optional type (logic / wire / reg / bit …)
        signal_type = "logic"

        if (
            not context.eof()
            and context.current().value in PortParser._TYPES
        ):
            signal_type = context.advance().value

        # optional signedness modifier (signed / unsigned)
        #
        # IEEE 1800 allows: input logic signed [7:0] name
        #                   input logic unsigned [7:0] name
        # We consume the keyword and embed it into signal_type so that
        # the TypeResolver's _infer_signedness() can detect "signed" in
        # the type string.
        if (
            not context.eof()
            and context.current().token_type == RTLTokenType.IDENTIFIER
            and context.current().value in PortParser._SIGNEDNESS
        ):
            signedness = context.advance().value
            signal_type = f"{signal_type} {signedness}"

        # optional packed range
        packed_range = None

        if PackedRangeParser.matches(context):
            packed_range = PackedRangeParser.parse(context)

        # identifier
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
            start_token.source_location,
        )

        return node
