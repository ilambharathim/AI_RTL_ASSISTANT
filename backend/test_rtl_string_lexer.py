from app.domain.rtl_tokens import RTLTokenType
from app.parsers.rtl.lexer import RTLLexer

lexer = RTLLexer()

result = lexer.tokenize('"hello world"')

assert result.successful

assert len(result.tokens) == 2

assert result.tokens[0].token_type == RTLTokenType.STRING
assert result.tokens[0].value == "hello world"

assert result.tokens[1].token_type == RTLTokenType.END_OF_FILE

print("RTL string lexer test passed.")
