from app.domain.rtl_tokens import RTLTokenType
from app.parsers.rtl.lexer import RTLLexer

lexer = RTLLexer()

#
# Integer literals
#
for example in (
    "123",
    "32'd100",
    "8'hFF",
    "16'sd12",
):
    result = lexer.tokenize(example)

    assert result.successful
    assert result.tokens[0].token_type == RTLTokenType.NUMBER

#
# Real literals
#
for example in (
    "3.14",
    "0.5",
    "10.",
    "1e6",
    "5.2e-3",
    "2E+8",
):
    result = lexer.tokenize(example)

    assert result.successful
    assert result.tokens[0].token_type == RTLTokenType.REAL_NUMBER

#
# Time literals
#
for example in (
    "10ns",
    "5ps",
    "100fs",
    "2us",
    "50ms",
    "1s",
):
    result = lexer.tokenize(example)

    assert result.successful
    assert result.tokens[0].token_type == RTLTokenType.TIME_LITERAL

print("RTL number lexer test passed.")
