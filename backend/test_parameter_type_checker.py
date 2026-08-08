from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    ParameterDeclaration,
)

from app.ast.expression import IdentifierExpression

from app.semantics.semantic_model import SemanticModel

from app.semantics.passes.parameter_type_checker import (
    ParameterTypeChecker,
)


def test_parameter_type_checker():

    tree = CompilationUnit(
        declarations=(
            ModuleDeclaration(
                name="top",
                ports=(),
                members=(
                    ParameterDeclaration(
                        name="WIDTH",
                        value=IdentifierExpression(
                            "MISSING",
                        ),
                    ),
                ),
            ),
        ),
    )

    model = SemanticModel()

    ParameterTypeChecker().check(
        tree,
        model,
    )

    assert len(model.diagnostics) == 1

    diagnostic = model.diagnostics[0]

    assert diagnostic.code == "RIVA1001"

    assert diagnostic.category == "Semantic"

    assert diagnostic.severity == "error"

    assert diagnostic.message == (
        "Identifier 'MISSING' is not declared."
    )
