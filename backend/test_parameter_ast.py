from app.ast.parameter_declaration import ParameterDeclaration

parameter = ParameterDeclaration(
    name="WIDTH",
    value="8",
)

assert parameter.kind == "ParameterDeclaration"
assert parameter.name == "WIDTH"
assert parameter.value == "8"

print("ParameterDeclaration AST test passed.")
