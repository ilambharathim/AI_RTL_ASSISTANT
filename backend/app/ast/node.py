"""
Base AST Node.
"""

from dataclasses import dataclass, field

from app.common.source_location import (
    SourceLocation,
)


@dataclass(frozen=True, slots=True)
class ASTNode:

    kind: str

    location: SourceLocation | None = field(
        default=None,
        init=False,
    )
