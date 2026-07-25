from app.parsers.specification.lexer import SpecificationLexer

text = """

Module Name: mux2to1

Inputs:
a
b
sel

Outputs:
y

"""

lexer = SpecificationLexer(text)

tokens = lexer.tokenize()

print("\n========== TOKENS ==========\n")

for token in tokens:
    print(token)
