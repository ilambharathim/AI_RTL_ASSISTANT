from app.ast.generate_block import GenerateBlock

node = GenerateBlock(
    members=(),
)

assert node.kind == "GenerateBlock"
assert node.members == ()

print("GenerateBlock AST test passed.")
