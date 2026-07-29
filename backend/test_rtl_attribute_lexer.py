from app.domain.rtl_tokens import RTLTokenType
from app.parsers.rtl.lexer import RTLLexer

lexer = RTLLexer()

examples = (
    "(* keep *)",
    '(* ram_style = "block" *)',
    "(* dont_touch *)",
)

for example in examples:

    result = lexer.tokenize(example)

    assert result.successful

    assert result.tokens[0].token_type == RTLTokenType.ATTRIBUTE

print("RTL attribute lexer test passed.")
