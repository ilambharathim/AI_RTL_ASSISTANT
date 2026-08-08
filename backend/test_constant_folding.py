from app.ast.expression import (
    LiteralExpression,
    BinaryExpression,
)

from app.semantics.passes.constant_folding import (
    ConstantFolding,
)

expr = BinaryExpression(
    "+",
    LiteralExpression("4"),
    LiteralExpression("5"),
)

folded = ConstantFolding().fold(expr)

assert isinstance(
    folded,
    LiteralExpression,
)

assert folded.value == "9"

print("ConstantFolding test passed.")
