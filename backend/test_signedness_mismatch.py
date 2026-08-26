from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    SignalDeclaration,
    ProceduralAssignment,
)

from app.ast.expression import (
    IdentifierExpression,
)

from app.semantics.semantic_model import (
    SemanticModel,
)

from app.diagnostics.rules.signedness_mismatch import (
    SignednessMismatchRule,
)


def make_tree():

    return CompilationUnit(
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
                    ProceduralAssignment(
                        target="a",
                        operator="=",
                        expression=IdentifierExpression(
                            "b",
                        ),
                    ),
                ),
            ),
        ),
    )


def test_signedness_mismatch():

    model = SemanticModel()

    model.types["a"] = {
        "type": "logic",
        "width": 8,
        "signed": True,
    }

    model.types["b"] = {
        "type": "logic",
        "width": 8,
        "signed": False,
    }

    model.syntax_tree = make_tree()

    diagnostics = SignednessMismatchRule().run(
        model,
    )

    assert len(diagnostics) == 1

    diagnostic = diagnostics[0]

    assert diagnostic.code == "RIVA3002"
    assert diagnostic.category == "Width"
    assert diagnostic.severity == "warning"

    assert diagnostic.message == (
        "Signedness mismatch: "
        "a (signed) <- "
        "b (unsigned)"
    )


def test_matching_signedness_has_no_diagnostic():

    model = SemanticModel()

    model.types["a"] = {
        "type": "logic",
        "width": 8,
        "signed": True,
    }

    model.types["b"] = {
        "type": "logic",
        "width": 8,
        "signed": True,
    }

    model.syntax_tree = make_tree()

    diagnostics = SignednessMismatchRule().run(
        model,
    )

    assert diagnostics == []


def test_signedness_mismatch_from_binary_expression():

    from app.ast.expression import BinaryExpression

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
                    SignalDeclaration(
                        signal_type="logic",
                        packed_range=None,
                        name="c",
                    ),
                    ProceduralAssignment(
                        target="a",
                        operator="=",
                        expression=BinaryExpression(
                            "+",
                            IdentifierExpression("b"),
                            IdentifierExpression("c"),
                        ),
                    ),
                ),
            ),
        ),
    )

    model = SemanticModel()

    model.types["a"] = {
        "type": "logic",
        "width": 8,
        "signed": True,
    }

    model.types["b"] = {
        "type": "logic",
        "width": 8,
        "signed": False,
    }

    model.types["c"] = {
        "type": "logic",
        "width": 8,
        "signed": False,
    }

    model.syntax_tree = tree

    diagnostics = SignednessMismatchRule().run(
        model,
    )

    assert len(diagnostics) == 1

    assert diagnostics[0].code == "RIVA3002"


def test_signedness_mismatch_from_literal_expression():

    from app.ast.expression import LiteralExpression

    tree = CompilationUnit(
        declarations=(
            ModuleDeclaration(
                name="top",
                ports=(),
                members=(
                    SignalDeclaration(
                        signal_type="logic",
                        packed_range=None,
                        name="a",
                    ),
                    ProceduralAssignment(
                        target="a",
                        operator="=",
                        expression=LiteralExpression(
                            "42",
                        ),
                    ),
                ),
            ),
        ),
    )

    model = SemanticModel()

    model.types["a"] = {
        "type": "logic",
        "width": 32,
        "signed": False,
    }

    model.syntax_tree = tree

    diagnostics = SignednessMismatchRule().run(
        model,
    )

    assert len(diagnostics) == 1

    assert diagnostics[0].code == "RIVA3002"


def test_binary_expression_with_signed_operand_is_signed():

    from app.ast.expression import BinaryExpression

    tree = CompilationUnit(
        declarations=(
            ModuleDeclaration(
                name="top",
                ports=(),
                members=(
                    SignalDeclaration(
                        signal_type="logic",
                        packed_range=None,
                        name="a",
                    ),
                    SignalDeclaration(
                        signal_type="logic",
                        packed_range=None,
                        name="b",
                    ),
                    SignalDeclaration(
                        signal_type="logic signed",
                        packed_range=None,
                        name="c",
                    ),
                    ProceduralAssignment(
                        target="a",
                        operator="=",
                        expression=BinaryExpression(
                            "+",
                            IdentifierExpression("b"),
                            IdentifierExpression("c"),
                        ),
                    ),
                ),
            ),
        ),
    )

    model = SemanticModel()

    model.types["a"] = {
        "type": "logic",
        "width": 8,
        "signed": False,
    }

    model.types["b"] = {
        "type": "logic",
        "width": 8,
        "signed": False,
    }

    model.types["c"] = {
        "type": "logic",
        "width": 8,
        "signed": True,
    }

    model.syntax_tree = tree

    diagnostics = SignednessMismatchRule().run(
        model,
    )

    assert len(diagnostics) == 1

    assert diagnostics[0].code == "RIVA3002"
