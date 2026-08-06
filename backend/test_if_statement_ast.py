from app.ast.expression import IdentifierExpression
from app.ast.if_statement import IfStatement
from app.ast.procedural_assignment import ProceduralAssignment

then_stmt = ProceduralAssignment(
    target="sum",
    operator="=",
    expression=IdentifierExpression("a"),
)

else_stmt = ProceduralAssignment(
    target="sum",
    operator="=",
    expression=IdentifierExpression("b"),
)

node = IfStatement(
    condition="enable",
    then_branch=(then_stmt,),
    else_branch=(else_stmt,),
)

assert node.kind == "IfStatement"
assert node.condition == "enable"
assert len(node.then_branch) == 1
assert len(node.else_branch) == 1

assert node.then_branch[0].expression.name == "a"
assert node.else_branch[0].expression.name == "b"

print("IfStatement AST test passed.")
