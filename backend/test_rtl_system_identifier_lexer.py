from app.domain.rtl_tokens import RTLTokenType
from app.parsers.rtl.lexer import RTLLexer

lexer = RTLLexer()

examples = (
    "$display",
    "$finish",
    "$monitor",
    "$clog2",
    "$bits",
    "$random",
    "$urandom",
    "$time",
)

for example in examples:

    result = lexer.tokenize(example)

    assert result.successful

    assert result.tokens[0].token_type == RTLTokenType.SYSTEM_IDENTIFIER

print("RTL system identifier lexer test passed.")
