from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
)

from app.ast.module_instance import ModuleInstance

from app.elaboration.validation.instance_validator import (
    InstanceValidator,
)

tree = CompilationUnit(

    declarations=(

        ModuleDeclaration(
            name="adder",
            ports=(),
            members=(),
        ),

        ModuleDeclaration(
            name="top",
            ports=(),
            members=(

                ModuleInstance(

                    module_name="adder",

                    parameter_overrides=(),

                    instance_name="u0",

                    connections=(),

                ),

            ),
        ),

    ),

)

errors = InstanceValidator().validate(
    tree,
)

assert errors == []

print("InstanceValidator test passed.")

