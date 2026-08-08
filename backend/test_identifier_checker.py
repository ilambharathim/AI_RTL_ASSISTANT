from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    ParameterDeclaration,
)

from app.ast.expression import IdentifierExpression

from app.semantics.semantic_model import SemanticModel
from app.semantics.passes.identifier_checker import (
    IdentifierChecker,
)


def test_identifier_checker():

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

    IdentifierChecker().check(
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

    assert diagnostic.message == (
        "Identifier 'MISSING' is not declared."
    )


if __name__ == "__main__":
    test_identifier_checker()
    print("IdentifierChecker test passed.")
