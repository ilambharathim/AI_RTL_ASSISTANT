from app.parsers.specification.tokens import Token
from app.parsers.specification.token_types import TokenType


token = Token(
    type=TokenType.SECTION_HEADER,
    value="Inputs",
    line=12,
    column=1,
    source_file="specification.txt",
    section="Interface"
)

print("\n========== TOKEN ==========\n")
print(token)

print("\nType        :", token.type)
print("Value       :", token.value)
print("Line        :", token.line)
print("Column      :", token.column)
print("Source File :", token.source_file)
print("Section     :", token.section)
