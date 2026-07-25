from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class Requirement:
    """
    Represents one engineering requirement extracted
    from a specification document.

    Every requirement must have a unique ID so that
    diagnostics and reports can reference it.
    """

    requirement_id: str

    category: str

    description: str

    condition: Optional[str] = None

    expected_result: Optional[str] = None

    priority: str = "MEDIUM"

    source_section: Optional[str] = None

    verification_status: str = "NOT_VERIFIED"
