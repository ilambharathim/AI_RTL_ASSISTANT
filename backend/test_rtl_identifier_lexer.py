from app.domain.rtl_tokens import RTLTokenType
from app.parsers.rtl.lexer import RTLLexer

lexer = RTLLexer()

#
# Normal identifier
#

result = lexer.tokenize("my_signal")

assert result.successful

assert result.tokens[0].token_type == RTLTokenType.IDENTIFIER
assert result.tokens[0].value == "my_signal"

#
# Escaped identifier
#

result = lexer.tokenize("\\my.signal ")

assert result.successful

assert result.tokens[0].token_type == RTLTokenType.IDENTIFIER
assert result.tokens[0].value == "\\my.signal"

print("RTL identifier lexer test passed.")
