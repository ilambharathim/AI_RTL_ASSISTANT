"""
Engineering requirement domain model.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.shared.source_location import SourceLocation


@dataclass(slots=True)
class Requirement:
    """
    Represents one engineering requirement extracted from a specification.

    Every requirement has a stable identifier and may preserve the exact
    source location from which it was derived.
    """

    requirement_id: str
    category: str
    description: str
    condition: str | None = None
    expected_result: str | None = None
    priority: str = "MEDIUM"
    source_section: str | None = None
    verification_status: str = "NOT_VERIFIED"
    source_location: SourceLocation = field(default_factory=SourceLocation)

    def __post_init__(self) -> None:
        if not isinstance(self.source_location, SourceLocation):
            raise TypeError(
                "source_location must be a SourceLocation."
            )
