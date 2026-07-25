from app.parsers.specification.token_builder import TokenBuilder
from app.parsers.specification.token_types import TokenType


def main():

    token = TokenBuilder.build(
        token_type=TokenType.SECTION_HEADER,
        value="Inputs",
        line=12,
        column=1,
        source_file="specification.txt",
        section="Interface",
    )

    print("\n===== TOKEN BUILDER =====\n")

    print(token)

    print()

    print("Type       :", token.type)
    print("Value      :", token.value)
    print("Line       :", token.line)
    print("Column     :", token.column)
    print("Source     :", token.source_file)
    print("Section    :", token.section)


if __name__ == "__main__":
    main()