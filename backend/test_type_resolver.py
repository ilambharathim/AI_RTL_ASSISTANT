from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    SignalDeclaration,
)

from app.semantics.semantic_model import SemanticModel
from app.semantics.passes.type_resolver import TypeResolver


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
            ),
        ),
    ),
)

model = SemanticModel()

TypeResolver().resolve(
    tree,
    model,
)

assert "a" in model.types
assert model.types["a"]["type"] == "logic"
assert model.types["a"]["packed_range"] is None

print("TypeResolver test passed.")
