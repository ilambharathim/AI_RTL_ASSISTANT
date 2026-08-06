from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    ModuleInstance,
)

from app.semantics.semantic_model import SemanticModel

from app.elaboration.modules.module_resolver import (
    ModuleResolver,
)

from app.elaboration.instances.instance_resolver import (
    InstanceResolver,
)

child = ModuleDeclaration(
    name="child",
    ports=(),
    members=(),
)

top = ModuleDeclaration(
    name="top",
    ports=(),
    members=(
        ModuleInstance(
            module_name="child",
            parameter_overrides=(),
            instance_name="u0",
            connections=(),
        ),
    ),
)

tree = CompilationUnit(
    declarations=(
        child,
        top,
    ),
)

model = SemanticModel()

ModuleResolver().resolve(
    tree,
    model,
)

InstanceResolver().resolve(
    tree,
    model,
)

modules = model.elaboration.elaborated_modules

assert "top" in modules

assert "u0" in modules["top"].instances

instance = modules["top"].instances["u0"]

assert instance.instance_name == "u0"

assert instance.module_name == "child"

print("Typed InstanceResolver test passed.")
