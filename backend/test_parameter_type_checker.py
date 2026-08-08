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

    assert (
        model.diagnostics[0]["kind"]
        == "UnknownParameterType"
    )

    assert (
        model.diagnostics[0]["parameter"]
        == "WIDTH"
    )

    assert (
        model.diagnostics[0]["identifier"]
        == "MISSING"
    )


if __name__ == "__main__":
    test_parameter_type_checker()
    print("ParameterTypeChecker test passed.")
