"""
Severity levels for RIVA diagnostics.
"""

from enum import Enum


class DiagnosticSeverity(str, Enum):
    """
    Stable severity values shared by parsers, rules, and verification engines.
    """

    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
