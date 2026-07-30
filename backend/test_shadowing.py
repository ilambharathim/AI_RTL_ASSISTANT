from app.parsers.rtl.lexer import RTLLexer
from app.parsers.rtl.parser import RTLParser

from app.semantics.visitors.scope_builder import ScopeBuilder

lexer = RTLLexer()

parser = RTLParser()

tokens = lexer.tokenize(
"""
module demo;

logic a;

always_comb begin

logic a;

end

endmodule
"""
)

tree = parser.parse(tokens.tokens)

builder = ScopeBuilder()

builder.build(tree.syntax_tree)

assert len(builder.collector.diagnostics) == 1

print("Shadowing detection test passed.")
