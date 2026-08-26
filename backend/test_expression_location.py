from app.ast.expression import (
    IdentifierExpression,
    LiteralExpression,
    UnaryExpression,
    BinaryExpression,
    FunctionCallExpression,
)
from app.common.source_location import SourceLocation


location = SourceLocation(
    line=10,
    column=5,
    file="test.sv",
)


def check_location(node, expected):
    assert hasattr(node, "location")
    assert node.location == expected


identifier = IdentifierExpression("a")
check_location(identifier, None)

literal = LiteralExpression("5")
check_location(literal, None)

unary = UnaryExpression(
    "-",
    identifier,
)
check_location(unary, None)

binary = BinaryExpression(
    "+",
    identifier,
    literal,
)
check_location(binary, None)

function = FunctionCallExpression(
    "foo",
    (identifier,),
)
check_location(function, None)


# Verify that frozen AST nodes still permit the parser's
# existing object.__setattr__ source-location mechanism.
object.__setattr__(
    identifier,
    "location",
    location,
)

object.__setattr__(
    literal,
    "location",
    location,
)

object.__setattr__(
    unary,
    "location",
    location,
)

object.__setattr__(
    binary,
    "location",
    location,
)

object.__setattr__(
    function,
    "location",
    location,
)


for node in (
    identifier,
    literal,
    unary,
    binary,
    function,
):
    check_location(node, location)


print("Expression location test passed.")
