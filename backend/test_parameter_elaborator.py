from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    ModuleInstance,
)

from app.elaboration.parameters.parameter_elaborator import ParameterElaborator
from app.semantics.semantic_model import SemanticModel


tree = CompilationUnit(

    declarations=(

        ModuleDeclaration(

            name="top",

            ports=(),

            members=(

                ModuleInstance(

                    module_name="child",

                    parameter_overrides=(),

                    instance_name="u0",

                    connections=(),

                ),

            ),

        ),

    ),

)

model = SemanticModel()

ParameterElaborator().elaborate(

    tree,

    model,

)

assert "u0" in model.elaboration.instance_parameters

assert (

    model.elaboration.instance_parameters["u0"]

    == {}

)

print("ParameterElaborator test passed.")

