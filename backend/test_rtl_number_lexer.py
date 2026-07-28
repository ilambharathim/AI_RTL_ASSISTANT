from app.domain.rtl_tokens import RTLTokenType
from app.parsers.rtl.lexer import RTLLexer

lexer = RTLLexer()

examples = [
    "12345",
    "8'hFF",
    "16'd255",
    "4'b1010",
    "32'o777",
    "'hABCD",
    "'d10",
    "'b101",
    "32'shFFFF",
    "8'sd10",
    "16'sb1010",
    "4'so7",
]

for example in examples:

    result = lexer.tokenize(example)

    assert result.successful

    assert result.tokens[0].token_type == RTLTokenType.NUMBER
    assert result.tokens[0].value == example

    assert result.tokens[1].token_type == RTLTokenType.END_OF_FILE

print("RTL number lexer test passed.")
