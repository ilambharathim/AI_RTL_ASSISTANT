from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    ModuleInstance,
)

from app.elaboration.hierarchy.hierarchy_elaborator import HierarchyElaborator
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

HierarchyElaborator().elaborate(

    tree,

    model,

)

assert model.elaboration.hierarchy == {

    "top": [

        "u0",

    ],

}

print("HierarchyElaborator test passed.")

