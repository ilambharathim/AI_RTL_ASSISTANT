from app.ast import (
    CompilationUnit,
    ParameterDeclaration,
)

from app.ast.expression import LiteralExpression

from app.semantics.semantic_model import SemanticModel
from app.semantics.evaluation.constant_evaluator import ConstantEvaluator

tree = CompilationUnit(

    declarations=(

        ParameterDeclaration(

            name="WIDTH",

            value=LiteralExpression("8"),

        ),

    ),

)

model = SemanticModel()

ConstantEvaluator().evaluate(
    tree,
    model,
)

assert model.constant_values["WIDTH"] == 8

print(model.constant_values)

print("ConstantEvaluator test passed.")
