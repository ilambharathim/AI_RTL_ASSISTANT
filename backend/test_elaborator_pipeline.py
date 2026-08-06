from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    ParameterDeclaration,
)

from app.ast.expression import LiteralExpression
from app.ast.module_instance import ModuleInstance
from app.ast.parameter_override import ParameterOverride

from app.elaboration.elaborator import Elaborator
from app.semantics.semantic_model import SemanticModel


adder = ModuleDeclaration(

    name="adder",

    ports=(),

    members=(

        ParameterDeclaration(

            name="WIDTH",

            value=LiteralExpression("8"),

        ),

    ),

)

top = ModuleDeclaration(

    name="top",

    ports=(),

    members=(

        ModuleInstance(

            module_name="adder",

            parameter_overrides=(

                ParameterOverride(

                    name="WIDTH",

                    expression=LiteralExpression("32"),

                ),

            ),

            instance_name="u0",

            connections=(),

        ),

    ),

)

tree = CompilationUnit(

    declarations=(

        adder,

        top,

    ),

)

model = SemanticModel()

Elaborator().elaborate(

    tree,

    model,

)

assert model.elaboration.instance_parameters["u0"]["WIDTH"].value == "32"

print("Elaborator pipeline test passed.")

