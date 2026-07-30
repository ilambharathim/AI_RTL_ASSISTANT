from app.parsers.rtl.lexer import RTLLexer
from app.parsers.rtl.parser import RTLParser

from app.semantics.visitors.scope_builder import ScopeBuilder

lexer = RTLLexer()

parser = RTLParser()

tokens = lexer.tokenize(
"""
module demo;

always_comb begin

begin

a = b;

end

end

endmodule
"""
)

tree = parser.parse(tokens.tokens)

builder = ScopeBuilder()

root = builder.build(
    tree.syntax_tree,
)

assert len(root.children) == 1

module_scope = root.children[0]

assert module_scope.name == "demo"

assert len(module_scope.children) == 1

always_scope = module_scope.children[0]

assert always_scope.kind.value == "PROCEDURAL"

assert len(always_scope.children) == 1

print("Scope builder test passed.")
