from app.domain.rtl_tokens import RTLTokenType
from app.parsers.rtl.lexer import RTLLexer

lexer = RTLLexer()

result = lexer.tokenize("12345")

assert result.successful

assert len(result.tokens) == 2

assert result.tokens[0].token_type == RTLTokenType.NUMBER
assert result.tokens[0].value == "12345"

assert result.tokens[1].token_type == RTLTokenType.END_OF_FILE

print("RTL number lexer test passed.")
