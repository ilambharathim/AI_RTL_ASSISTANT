from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
)

from app.elaboration.module_elaborator import ModuleElaborator

tree = CompilationUnit(
    declarations=(
        ModuleDeclaration(
            name="top",
            ports=(),
            members=(),
        ),
    ),
)

hierarchy = ModuleElaborator().elaborate(tree)

assert "top" in hierarchy

print("Module elaborator test passed.")
