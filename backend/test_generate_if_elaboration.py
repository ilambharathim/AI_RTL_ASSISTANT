from app.ast import (
    GenerateIf,
)

from app.ast.expression import (
    LiteralExpression,
)

from app.elaboration.generate.generate_elaborator import (
    GenerateElaborator,
)

class Dummy:

    def __init__(self):
        self.constant_values = {}

elab = GenerateElaborator()

node = GenerateIf(

    condition=LiteralExpression("1"),

    true_members=("TRUE",),

    false_members=("FALSE",),

)

result = elab._generate_if(

    node,

    Dummy(),

)

assert result == ["TRUE"]

node = GenerateIf(

    condition=LiteralExpression("0"),

    true_members=("TRUE",),

    false_members=("FALSE",),

)

result = elab._generate_if(

    node,

    Dummy(),

)

assert result == ["FALSE"]

print("Generate-if elaboration test passed.")

