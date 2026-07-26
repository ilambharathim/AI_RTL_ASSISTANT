"""
Stable diagnostic-code catalog for deterministic specification validation.
"""

from enum import Enum


class SpecificationValidationDiagnosticCode(str, Enum):
    """
    Released machine-readable codes for specification validation diagnostics.

    Values are stable external contracts and must not be renamed or reused.
    """

    MISSING_PROJECT_NAME = "SPEC-VAL-001"
    MISSING_MODULE_NAME = "SPEC-VAL-002"
    MISSING_PORTS = "SPEC-VAL-003"
    MISSING_REQUIREMENTS = "SPEC-VAL-004"
    INVALID_PORT_DIRECTION = "SPEC-VAL-005"
    INVALID_PORT_WIDTH = "SPEC-VAL-006"
    DUPLICATE_PORT_NAME = "SPEC-VAL-007"
    DUPLICATE_REQUIREMENT_ID = "SPEC-VAL-008"
    EMPTY_REQUIREMENT_DESCRIPTION = "SPEC-VAL-009"
