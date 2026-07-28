from app.domain.rtl_tokens import RTLTokenType
from app.parsers.rtl.lexer import RTLLexer

lexer = RTLLexer()

result = lexer.tokenize("a===b")

assert result.successful

assert len(result.tokens) == 4

assert result.tokens[0].token_type == RTLTokenType.IDENTIFIER
assert result.tokens[0].value == "a"

assert result.tokens[1].token_type == RTLTokenType.OPERATOR
assert result.tokens[1].value == "==="

assert result.tokens[2].token_type == RTLTokenType.IDENTIFIER
assert result.tokens[2].value == "b"

assert result.tokens[3].token_type == RTLTokenType.END_OF_FILE

print("RTL operator lexer test passed.")
