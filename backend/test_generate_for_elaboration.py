from app.ast import GenerateFor
from app.ast.expression import LiteralExpression

from app.elaboration.generate.generate_elaborator import (
    GenerateElaborator,
)


class Dummy:

    constant_values = {}


node = GenerateFor(

    variable="i",

    initializer=LiteralExpression("0"),

    condition=LiteralExpression("4"),

    update=LiteralExpression("i+1"),

    members=("INSTANCE",),

)

expanded = GenerateElaborator()._generate_for(

    node,

    Dummy(),

)

assert len(expanded) == 4

print("Generate-for elaboration test passed.")

