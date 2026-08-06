"""
Diagnostic catalog definitions.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DiagnosticDefinition:

    code: str

    category: str

    severity: str

    title: str

    message: str

    explanation: str

    suggestion: str
