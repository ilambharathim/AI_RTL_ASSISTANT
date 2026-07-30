from app.ast.case_statement import (
    CaseItem,
    CaseStatement,
)

item0 = CaseItem(
    label="0",
    statements=(),
)

item1 = CaseItem(
    label="default",
    statements=(),
)

node = CaseStatement(
    expression="opcode",
    items=(item0, item1),
)

assert node.kind == "CaseStatement"
assert node.expression == "opcode"

assert len(node.items) == 2

assert node.items[0].label == "0"
assert node.items[1].label == "default"

print("CaseStatement AST test passed.")
