"""
Stable diagnostic codes emitted by the specification semantic builder.
"""

from enum import Enum


class SpecificationSemanticDiagnosticCode(str, Enum):
    """
    Machine-readable codes for specification semantic interpretation.

    Existing values must not be renamed or reused for different meanings after
    release because reports, suppressions, and external integrations may depend
    on them.
    """

    UNKNOWN_DOCUMENT_ENTRY = "SPEC-SEM-001"
    UNKNOWN_SECTION = "SPEC-SEM-002"

    DUPLICATE_METADATA_FIELD = "SPEC-SEM-003"
    EMPTY_METADATA_VALUE = "SPEC-SEM-004"

    INVALID_SECTION_ENTRY = "SPEC-SEM-005"
    EMPTY_SECTION = "SPEC-SEM-006"

    INVALID_PORT_DECLARATION = "SPEC-SEM-007"
    INVALID_PORT_NAME = "SPEC-SEM-008"
    DUPLICATE_PORT = "SPEC-SEM-009"
    INVALID_PORT_WIDTH = "SPEC-SEM-010"

    EMPTY_REQUIREMENT = "SPEC-SEM-011"
    MISSING_MODULE_NAME = "SPEC-SEM-012"
