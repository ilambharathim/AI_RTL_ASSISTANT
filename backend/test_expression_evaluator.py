from app.ast.expression import (
    LiteralExpression,
    BinaryExpression,
)

from app.semantics.passes.expression_evaluator import (
    ExpressionEvaluator,
)

expr = BinaryExpression(
    "+",
    LiteralExpression("7"),
    LiteralExpression("5"),
)

assert ExpressionEvaluator.evaluate(expr) == 12

print("ExpressionEvaluator test passed.")
