from app.ast.always_block import AlwaysBlock

block = AlwaysBlock(
    block_type="always_comb",
    sensitivity="*",
    statements=(),
)

assert block.kind == "AlwaysBlock"
assert block.block_type == "always_comb"
assert block.sensitivity == "*"
assert len(block.statements) == 0

print("AlwaysBlock AST test passed.")
