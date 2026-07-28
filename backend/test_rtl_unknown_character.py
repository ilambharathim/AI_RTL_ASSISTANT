from app.parsers.rtl.lexer import RTLLexer

lexer = RTLLexer()

result = lexer.tokenize("module @ adder")

assert len(result.diagnostics) == 1
assert result.diagnostics[0].code == "LEX004"

print("RTL unknown character recovery test passed.")
