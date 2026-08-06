from app.ast import (
    GenerateFor,
    ModuleInstance,
)

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

    members=(

        ModuleInstance(

            module_name="adder",

            parameter_overrides=(),

            instance_name="u",

            connections=(),

        ),

    ),

)

instances = GenerateElaborator()._generate_for(

    node,

    Dummy(),

)

assert len(instances) == 4

assert instances[0].instance_name == "u_0"
assert instances[1].instance_name == "u_1"
assert instances[2].instance_name == "u_2"
assert instances[3].instance_name == "u_3"

print("Generate-for cloning test passed.")

