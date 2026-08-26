from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    SignalDeclaration,
)

from app.semantics.semantic_model import SemanticModel
from app.semantics.passes.signedness_resolver import (
    SignednessResolver,
)
from app.semantics.types.rtl.rtl_type import RTLType


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
                ),
            ),
        ),
    )


def test_signedness_resolver():

    model = SemanticModel()

    SignednessResolver().resolve(
        make_tree(),
        model,
    )

    assert model.types["a"]["signed"] is True
    assert model.types["b"]["signed"] is False


def test_signedness_resolver_updates_canonical_types():

    model = SemanticModel()

    model.set_semantic_type(
        "a",
        RTLType(
            name="logic signed",
            width=8,
            signed=False,
            packed=False,
        ),
    )

    model.set_semantic_type(
        "b",
        RTLType(
            name="logic",
            width=8,
            signed=True,
            packed=False,
        ),
    )

    SignednessResolver().resolve(
        make_tree(),
        model,
    )

    a = model.get_semantic_type("a")
    b = model.get_semantic_type("b")

    assert a is not None
    assert b is not None

    assert a.signed is True
    assert b.signed is False

    assert a.width == 8
    assert b.width == 8
