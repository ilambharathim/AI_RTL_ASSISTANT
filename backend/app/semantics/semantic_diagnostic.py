"""
Semantic diagnostics.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class SemanticDiagnostic:

    message: str
