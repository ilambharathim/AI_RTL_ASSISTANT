from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    ProceduralAssignment,
)

from app.ast.expression import IdentifierExpression

from app.semantics.semantic_model import SemanticModel
from app.semantics.passes.identifier_checker import IdentifierChecker


def test_identifier_checker_records_unknown_identifier():

    tree = CompilationUnit(
        declarations=(
            ModuleDeclaration(
                name="top",
                ports=(),
                members=(
                    ProceduralAssignment(
                        target="a",
                        operator="=",
                        expression=IdentifierExpression(
                            "missing"
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
    assert diagnostic.message == "Identifier 'missing' is not declared."


if __name__ == "__main__":
    test_identifier_checker_records_unknown_identifier()
    print("Identifier diagnostic test passed.")
