from app.ast.expression import IdentifierExpression

from app.elaboration.utils.generate_substituter import (
    GenerateSubstituter,
)

expr = IdentifierExpression("i")

GenerateSubstituter.substitute(

    expr,

    "i",

    7,

)

assert expr.name == "7"

print("Generate substitution test passed.")

