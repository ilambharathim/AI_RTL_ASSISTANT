from app.ast import AlwaysBlock, ProceduralAssignment

from app.parsers.rtl.lexer import RTLLexer
from app.parsers.rtl.parser import RTLParser

from app.semantics.visitors.scope_builder import ScopeBuilder
from app.semantics.visitors.identifier_resolver import IdentifierResolver

lexer = RTLLexer()

parser = RTLParser()

tokens = lexer.tokenize(
"""
module demo;

logic a;

logic b;

always_comb begin

a = b;

end

endmodule
"""
)

tree = parser.parse(tokens.tokens)

builder = ScopeBuilder()

root = builder.build(
    tree.syntax_tree,
)

module_scope = root.children[0]

resolver = IdentifierResolver()

module = tree.syntax_tree.declarations[0]

always_block = None

for member in module.members:

    if isinstance(member, AlwaysBlock):

        always_block = member

        break

assert always_block is not None

assignment = always_block.statements[0]

assert isinstance(
    assignment,
    ProceduralAssignment,
)

resolver.visit(
    module_scope,
    assignment,
)

assert len(resolver.errors) == 0

print("Identifier resolution test passed.")
