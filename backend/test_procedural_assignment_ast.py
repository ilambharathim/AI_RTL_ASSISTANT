from app.ast.procedural_assignment import ProceduralAssignment

assignment = ProceduralAssignment(
    target="sum",
    operator="<=",
    expression="a & b",
)

assert assignment.kind == "ProceduralAssignment"
assert assignment.target == "sum"
assert assignment.operator == "<="
assert assignment.expression == "a & b"

print("ProceduralAssignment AST test passed.")
