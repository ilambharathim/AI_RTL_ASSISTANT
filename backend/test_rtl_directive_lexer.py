from app.domain.rtl_tokens import RTLTokenType
from app.parsers.rtl.lexer import RTLLexer

lexer = RTLLexer()

examples = (
    "`define",
    "`include",
    "`ifdef",
    "`ifndef",
    "`elsif",
    "`else",
    "`endif",
    "`timescale",
    "`default_nettype",
)

for example in examples:

    result = lexer.tokenize(example)

    assert result.successful

    assert result.tokens[0].token_type == RTLTokenType.DIRECTIVE

print("RTL directive lexer test passed.")
