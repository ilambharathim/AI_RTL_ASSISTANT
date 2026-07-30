from app.ast.signal_declaration import SignalDeclaration

signal = SignalDeclaration(
    signal_type="logic",
    name="carry",
)

assert signal.kind == "SignalDeclaration"
assert signal.signal_type == "logic"
assert signal.name == "carry"

print("SignalDeclaration AST test passed.")
