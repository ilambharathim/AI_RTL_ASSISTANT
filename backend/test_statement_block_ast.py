from app.ast.statement_block import StatementBlock
from app.ast.procedural_assignment import ProceduralAssignment

stmt1 = ProceduralAssignment(
    target="a",
    operator="=",
    expression="b",
)

stmt2 = ProceduralAssignment(
    target="c",
    operator="<=",
    expression="d",
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

print("StatementBlock AST test passed.")
