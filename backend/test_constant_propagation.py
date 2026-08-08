from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    ParameterDeclaration,
)

from app.ast.expression import LiteralExpression

from app.semantics.semantic_model import SemanticModel

from app.semantics.passes.constant_propagation import (
    ConstantPropagation,
)

tree = CompilationUnit(
    declarations=(
        ModuleDeclaration(
            name="top",
            ports=(),
            members=(
                ParameterDeclaration(
                    name="WIDTH",
                    value=LiteralExpression("8"),
                ),
            ),
        ),
    ),
)

model = SemanticModel()

ConstantPropagation().propagate(
    tree,
    model,
)

assert model.constant_values["WIDTH"] == 8

print("ConstantPropagation test passed.")
