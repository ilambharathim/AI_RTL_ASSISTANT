from app.parsers.specification.token_types import TokenType

print("\n===== Generic Token Types =====\n")

for token in TokenType:
    print(f"{token.name:20} -> {token.value}")

print("\nTotal:", len(TokenType))
