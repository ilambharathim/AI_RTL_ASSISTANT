"""
RIVA Generic Lexer Rules

These rules recognize generic document structures.

They are intentionally independent of
engineering semantics.
"""

from app.parsers.specification.classifier import LineType


class LexerRules:
    """
    Collection of reusable lexical rules.
    """

    @staticmethod
    def is_empty(line: str) -> bool:
        return line.strip() == ""

    @staticmethod
    def is_section_header(line: str) -> bool:
        line = line.strip()

        return (
            line.endswith(":")
            and ":" not in line[:-1]
        )

    @staticmethod
    def is_key_value(line: str) -> bool:
        line = line.strip()

        return ":" in line and not LexerRules.is_section_header(line)

    @staticmethod
    def is_list_item(line: str) -> bool:
        line = line.strip()

        return (
            bool(line)
            and " " not in line
            and ":" not in line
        )

    @staticmethod
    def classify(line: str) -> LineType:

        if LexerRules.is_empty(line):
            return LineType.EMPTY

        if LexerRules.is_section_header(line):
            return LineType.SECTION_HEADER

        if LexerRules.is_key_value(line):
            return LineType.KEY_VALUE

        if LexerRules.is_list_item(line):
            return LineType.LIST_ITEM

        return LineType.TEXT
