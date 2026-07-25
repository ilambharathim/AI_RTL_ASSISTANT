"""
Document Classifier

Delegates classification to LexerRules.
"""

from enum import Enum


class LineType(Enum):
    EMPTY = "EMPTY"
    SECTION_HEADER = "SECTION_HEADER"
    KEY_VALUE = "KEY_VALUE"
    LIST_ITEM = "LIST_ITEM"
    TEXT = "TEXT"


class DocumentClassifier:

    @staticmethod
    def classify(line: str) -> LineType:

        # Local import avoids circular dependency
        from app.parsers.specification.lexer_rules import LexerRules

        return LexerRules.classify(line)
