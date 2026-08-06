"""
Repair Suggestion.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class RepairSuggestion:

    diagnostic_code: str

    title: str

    explanation: str

    replacement: str | None = None

    confidence: int = 50

    reason: str = ""

    auto_apply: bool = False
