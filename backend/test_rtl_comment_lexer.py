from app.domain.rtl_tokens import RTLTokenType
from app.parsers.rtl.lexer import RTLLexer

lexer = RTLLexer()

result = lexer.tokenize("""
// comment
module test;
""")

assert result.successful

assert result.tokens[0].token_type == RTLTokenType.KEYWORD
assert result.tokens[0].value == "module"

assert result.tokens[1].token_type == RTLTokenType.IDENTIFIER
assert result.tokens[1].value == "test"

assert result.tokens[2].token_type == RTLTokenType.SYMBOL
assert result.tokens[2].value == ";"

assert result.tokens[3].token_type == RTLTokenType.END_OF_FILE

print("RTL comment lexer test passed.")
