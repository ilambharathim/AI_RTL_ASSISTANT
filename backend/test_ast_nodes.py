from app.ast.compilation_unit import CompilationUnit
from app.ast.module_declaration import ModuleDeclaration

module = ModuleDeclaration(
    name="adder",
    ports=(),
    members=(),
)

tree = CompilationUnit(
    declarations=(module,),
)

assert tree.kind == "CompilationUnit"

assert len(tree.declarations) == 1

assert tree.declarations[0].name == "adder"

assert tree.declarations[0].kind == "ModuleDeclaration"

print("AST infrastructure test passed.")
