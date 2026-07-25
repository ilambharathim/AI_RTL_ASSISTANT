"""
Stable diagnostic codes emitted by the generic specification parser.
"""

from enum import Enum


class SpecificationParserDiagnosticCode(str, Enum):
    """
    Machine-readable codes for generic specification grammar failures.

    Existing values must not be renamed or reused for different meanings after
    they are released because external reports and integrations may depend on
    them.
    """

    UNEXPECTED_TOKEN = "SPEC-PARSE-001"

    EXPECTED_SECTION_HEADER = "SPEC-PARSE-002"
    EMPTY_SECTION_HEADER = "SPEC-PARSE-003"
    EXPECTED_NEWLINE_AFTER_SECTION_HEADER = "SPEC-PARSE-004"

    EXPECTED_KEY = "SPEC-PARSE-005"
    EMPTY_KEY = "SPEC-PARSE-006"
    EXPECTED_COLON_AFTER_KEY = "SPEC-PARSE-007"
    EMPTY_VALUE = "SPEC-PARSE-008"
    EXPECTED_NEWLINE_AFTER_KEY_VALUE = "SPEC-PARSE-009"

    EXPECTED_LIST_ITEM = "SPEC-PARSE-010"
    EMPTY_LIST_ITEM = "SPEC-PARSE-011"
    EXPECTED_NEWLINE_AFTER_LIST_ITEM = "SPEC-PARSE-012"

    EXPECTED_TEXT = "SPEC-PARSE-013"
    EMPTY_TEXT = "SPEC-PARSE-014"
    EXPECTED_NEWLINE_AFTER_TEXT = "SPEC-PARSE-015"
