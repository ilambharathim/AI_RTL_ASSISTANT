from app.ast.expression import (
    IdentifierExpression,
    LiteralExpression,
    BinaryExpression,
)

left = IdentifierExpression("a")

right = LiteralExpression("5")

expr = BinaryExpression(
    operator="+",
    left=left,
    right=right,
)

assert expr.kind == "BinaryExpression"

assert expr.operator == "+"

assert expr.left.name == "a"

assert expr.right.value == "5"

print("Expression AST test passed.")
