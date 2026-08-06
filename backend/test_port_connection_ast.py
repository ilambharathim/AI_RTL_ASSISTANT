from app.ast.expression import IdentifierExpression
from app.ast.port_connection import PortConnection

node = PortConnection(

    port_name="clk",

    expression=IdentifierExpression("clock"),

)

assert node.kind == "PortConnection"

assert node.port_name == "clk"

assert node.expression.name == "clock"

print("PortConnection AST test passed.")
