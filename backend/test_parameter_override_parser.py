from app.domain.rtl_tokens.token import RTLToken
from app.domain.rtl_tokens.token_type import RTLTokenType

from app.shared.source_location import SourceLocation

from app.parsers.rtl.parser_context import ParserContext
from app.parsers.rtl.parsers.parameter_override_parser import (
    ParameterOverrideParser,
)

loc = SourceLocation(
    source_file="test.sv",
    line=1,
    column=1,
)

tokens = (

    RTLToken(
        RTLTokenType.SYMBOL,
        ".",
        loc,
    ),

    RTLToken(
        RTLTokenType.IDENTIFIER,
        "WIDTH",
        loc,
    ),

    RTLToken(
        RTLTokenType.SYMBOL,
        "(",
        loc,
    ),

    RTLToken(
        RTLTokenType.NUMBER,
        "32",
        loc,
    ),

    RTLToken(
        RTLTokenType.SYMBOL,
        ")",
        loc,
    ),

)

context = ParserContext(tokens)

node = ParameterOverrideParser.parse(
    context,
)

assert node.kind == "ParameterOverride"

assert node.name == "WIDTH"

assert node.expression.value == "32"

print("ParameterOverrideParser test passed.")

