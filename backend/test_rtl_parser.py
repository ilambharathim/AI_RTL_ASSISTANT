from app.ast.statement_block import StatementBlock
from app.parsers.rtl.lexer import RTLLexer
from app.parsers.rtl.parser import RTLParser

lexer = RTLLexer()
parser = RTLParser()

tokens = lexer.tokenize(
"""
module demo;

always_comb begin

begin

a = b;

c <= d;

end

end

endmodule
"""
)

result = parser.parse(tokens.tokens)

assert result.successful

module = result.syntax_tree.declarations[0]

block = module.members[0]

assert len(block.statements) == 1

nested = block.statements[0]

assert isinstance(
    nested,
    StatementBlock,
)

assert len(nested.statements) == 2

print("RTL nested begin/end parser test passed.")
