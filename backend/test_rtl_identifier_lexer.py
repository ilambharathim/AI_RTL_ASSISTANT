from app.domain.rtl_tokens import RTLTokenType
from app.parsers.rtl.lexer import RTLLexer

lexer = RTLLexer()

result = lexer.tokenize("module adder")

assert result.successful

assert len(result.tokens) == 3

assert result.tokens[0].token_type == RTLTokenType.KEYWORD
assert result.tokens[0].value == "module"

assert result.tokens[1].token_type == RTLTokenType.IDENTIFIER
assert result.tokens[1].value == "adder"

assert result.tokens[2].token_type == RTLTokenType.END_OF_FILE

print("RTL identifier lexer test passed.")
