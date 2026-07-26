"""
Engineering artifact metadata domain model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class Metadata:
    """
    Common metadata describing an engineering artifact.

    Timestamps are preserved only when explicitly supplied by the source or
    caller. RIVA does not invent a construction timestamp during deterministic
    parsing or semantic transformation.
    """

    project_name: str = ""
    module_name: str = ""
    description: str = ""
    language: str = ""
    version: str = "1.0"
    author: str | None = None
    organization: str | None = None
    source_file: str | None = None
    created_at: datetime | None = None
    tags: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.created_at is not None and not isinstance(
            self.created_at,
            datetime,
        ):
            raise TypeError("created_at must be a datetime or None.")
