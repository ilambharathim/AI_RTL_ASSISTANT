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


def test_parameter_type_checker_accepts_canonical_semantic_type():
    from app.ast import (
        CompilationUnit,
        ModuleDeclaration,
        ParameterDeclaration,
    )

    from app.ast.expression import IdentifierExpression

    from app.semantics.semantic_model import SemanticModel
    from app.semantics.types.rtl.rtl_type import RTLType
    from app.semantics.passes.parameter_type_checker import (
        ParameterTypeChecker,
    )

    tree = CompilationUnit(
        declarations=(
            ModuleDeclaration(
                name="top",
                ports=(),
                members=(
                    ParameterDeclaration(
                        name="WIDTH",
                        value=IdentifierExpression(
                            "BASE_WIDTH",
                        ),
                    ),
                ),
            ),
        ),
    )

    model = SemanticModel()

    model.set_semantic_type(
        "BASE_WIDTH",
        RTLType(
            name="logic",
            width=32,
            signed=False,
            packed=False,
        ),
    )

    ParameterTypeChecker().check(
        tree,
        model,
    )

    assert model.diagnostics == []
