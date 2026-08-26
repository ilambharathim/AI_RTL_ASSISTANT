from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    SignalDeclaration,
)

from app.semantics.semantic_analyzer import (
    SemanticAnalyzer,
)


def test_semantic_analyzer_resolves_signedness():

    tree = CompilationUnit(
        declarations=(
            ModuleDeclaration(
                name="top",
                ports=(),
                members=(
                    SignalDeclaration(
                        signal_type="logic signed",
                        packed_range=None,
                        name="a",
                    ),
                    SignalDeclaration(
                        signal_type="logic",
                        packed_range=None,
                        name="b",
                    ),
                ),
            ),
        ),
    )

    model = SemanticAnalyzer().analyze(
        tree,
    )

    assert model.types["a"]["signed"] is True
    assert model.types["b"]["signed"] is False
