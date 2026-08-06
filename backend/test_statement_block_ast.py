from app.ast.expression import IdentifierExpression
from app.ast.procedural_assignment import ProceduralAssignment
from app.ast.statement_block import StatementBlock

stmt1 = ProceduralAssignment(
    target="a",
    operator="=",
    expression=IdentifierExpression("b"),
)

stmt2 = ProceduralAssignment(
    target="c",
    operator="<=",
    expression=IdentifierExpression("d"),
)

block = StatementBlock(
    statements=(
        stmt1,
        stmt2,
    ),
)

assert block.kind == "StatementBlock"
assert len(block.statements) == 2

assert block.statements[0].target == "a"
assert block.statements[1].target == "c"

assert block.statements[0].expression.name == "b"
assert block.statements[1].expression.name == "d"

print("StatementBlock AST test passed.")
