from app.ast.generate_for import GenerateFor
from app.ast.expression import LiteralExpression

node = GenerateFor(

    variable="i",

    initializer=LiteralExpression("0"),

    condition=LiteralExpression("1"),

    update=LiteralExpression("i+1"),

    members=(),

)

assert node.kind == "GenerateFor"

assert node.variable == "i"

print("GenerateFor AST test passed.")
