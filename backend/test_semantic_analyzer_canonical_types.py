from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    SignalDeclaration,
    PackedRange,
)

from app.ast.expression import LiteralExpression

from app.semantics.semantic_analyzer import SemanticAnalyzer


def test_semantic_analyzer_populates_canonical_signal_type():
    tree = CompilationUnit(
        declarations=(
            ModuleDeclaration(
                name="top",
                ports=(),
                members=(
                    SignalDeclaration(
                        signal_type="logic",
                        packed_range=PackedRange(
                            LiteralExpression("7"),
                            LiteralExpression("0"),
                        ),
                        name="a",
                    ),
                    SignalDeclaration(
                        signal_type="logic signed",
                        packed_range=PackedRange(
                            LiteralExpression("15"),
                            LiteralExpression("0"),
                        ),
                        name="b",
                    ),
                ),
            ),
        ),
    )

    model = SemanticAnalyzer().analyze(tree)

    a = model.get_semantic_type("a")
    b = model.get_semantic_type("b")

    assert a is not None
    assert a.name == "logic"
    assert a.width == 8
    assert a.signed is False
    assert a.packed is True

    assert b is not None
    assert b.name == "logic signed"
    assert b.width == 16
    assert b.signed is True
    assert b.packed is True


def test_semantic_analyzer_keeps_legacy_types_synchronized():
    tree = CompilationUnit(
        declarations=(
            ModuleDeclaration(
                name="top",
                ports=(),
                members=(
                    SignalDeclaration(
                        signal_type="logic signed",
                        packed_range=PackedRange(
                            LiteralExpression("7"),
                            LiteralExpression("0"),
                        ),
                        name="a",
                    ),
                ),
            ),
        ),
    )

    model = SemanticAnalyzer().analyze(tree)

    canonical = model.get_semantic_type("a")
    legacy = model.types["a"]

    assert canonical.width == 8
    assert canonical.signed is True

    assert legacy["width"] == canonical.width
    assert legacy["signed"] == canonical.signed
    assert legacy["packed"] == canonical.packed
