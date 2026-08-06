from app.ast.expression import IdentifierExpression
from app.ast.procedural_assignment import ProceduralAssignment

assignment = ProceduralAssignment(
    target="sum",
    operator="<=",
    expression=IdentifierExpression("a"),
)

assert assignment.kind == "ProceduralAssignment"
assert assignment.target == "sum"
assert assignment.operator == "<="
assert assignment.expression.name == "a"

print("ProceduralAssignment AST test passed.")
