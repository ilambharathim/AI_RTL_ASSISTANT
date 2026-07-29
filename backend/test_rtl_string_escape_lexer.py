from app.parsers.rtl.lexer import RTLLexer

lexer = RTLLexer()

examples = (
    r'"hello\nworld"',
    r'"tab\tcharacter"',
    r'"quote: \""',
    r'"backslash\\test"',
)

for example in examples:

    result = lexer.tokenize(example)

    assert result.successful

print("RTL string escape lexer test passed.")
