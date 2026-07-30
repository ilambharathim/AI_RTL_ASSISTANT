from app.parsers.rtl.lexer import RTLLexer
from app.parsers.rtl.parser import RTLParser

from app.semantics.visitors.scope_builder import ScopeBuilder

lexer = RTLLexer()

parser = RTLParser()

tokens = lexer.tokenize(
"""
module demo;

parameter WIDTH = 8;

logic clk;

logic rst;

endmodule
"""
)

tree = parser.parse(tokens.tokens)

builder = ScopeBuilder()

root = builder.build(tree.syntax_tree)

assert "demo" in root.symbols

module_scope = root.children[0]

assert "WIDTH" in module_scope.symbols

assert "clk" in module_scope.symbols

assert "rst" in module_scope.symbols

print("Automatic symbol collection test passed.")
