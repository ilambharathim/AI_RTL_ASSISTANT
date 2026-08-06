from app.ast.parameter_override import ParameterOverride

from app.ast.expression import LiteralExpression

node = ParameterOverride(

    name="WIDTH",

    expression=LiteralExpression("32"),

)

assert node.kind == "ParameterOverride"

assert node.name == "WIDTH"

assert node.expression.value == "32"

print("ParameterOverride AST test passed.")

