from app.domain.rtl_tokens import RTLTokenType
from app.parsers.rtl.lexer import RTLLexer

lexer = RTLLexer()

result = lexer.tokenize("module adder();")

assert result.successful

expected_types = [
    RTLTokenType.KEYWORD,
    RTLTokenType.IDENTIFIER,
    RTLTokenType.SYMBOL,
    RTLTokenType.SYMBOL,
    RTLTokenType.SYMBOL,
    RTLTokenType.END_OF_FILE,
]

actual_types = [token.token_type for token in result.tokens]

assert actual_types == expected_types

expected_values = [
    "module",
    "adder",
    "(",
    ")",
    ";",
    "",
]

actual_values = [token.value for token in result.tokens]

assert actual_values == expected_values

print("RTL symbol lexer test passed.")
