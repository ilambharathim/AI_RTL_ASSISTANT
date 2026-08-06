from app.ast.signal_declaration import SignalDeclaration

signal = SignalDeclaration(
    signal_type="logic",
    packed_range=None,
    name="clk",
)

assert signal.kind == "SignalDeclaration"
assert signal.signal_type == "logic"
assert signal.packed_range is None
assert signal.name == "clk"

print("SignalDeclaration AST test passed.")
