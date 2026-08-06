"""
RIVA Diagnostic.
"""

from dataclasses import dataclass

from app.common.source_location import (
    SourceLocation,
)


@dataclass(slots=True)
class Diagnostic:

    #
    # Identity
    #
    code: str

    category: str

    severity: str

    #
    # User-facing text
    #
    message: str

    explanation: str = ""

    suggestion: str = ""

    #
    # Source information
    #
    location: SourceLocation | None = None

    related_locations: tuple = ()

    #
    # Repair
    #
    repairable: bool = False

    repair_id: str | None = None

    confidence: int = 0
