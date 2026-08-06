from app.ast.port_declaration import PortDeclaration

port = PortDeclaration(

    direction="input",

    signal_type="logic",

    packed_range=None,

    name="clk",

)

assert port.kind == "PortDeclaration"

assert port.direction == "input"

assert port.signal_type == "logic"

assert port.packed_range is None

assert port.name == "clk"

print("PortDeclaration AST test passed.")
