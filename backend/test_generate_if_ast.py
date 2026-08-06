from app.ast.generate_if import GenerateIf
from app.ast.expression import LiteralExpression

node = GenerateIf(

    condition=LiteralExpression("1"),

    true_members=(),

    false_members=(),

)

assert node.kind == "GenerateIf"

assert node.condition.value == "1"

print("GenerateIf AST test passed.")
