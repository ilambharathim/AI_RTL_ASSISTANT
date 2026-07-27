from __future__ import annotations

from dataclasses import dataclass, field

from app.shared.source_location import SourceLocation


@dataclass(slots=True)
class RTLNode:
    """
    Base class for every RTL Abstract Syntax Tree node.
    """

    source_location: SourceLocation = field(
        default_factory=SourceLocation
    )

    children: list["RTLNode"] = field(
        default_factory=list
    )

    def __post_init__(self) -> None:
        if not isinstance(
            self.source_location,
            SourceLocation,
        ):
            raise TypeError(
                "source_location must be a SourceLocation."
            )

    def add_child(self, node: "RTLNode") -> None:
        if not isinstance(node, RTLNode):
            raise TypeError(
                "child must be an RTLNode."
            )

        self.children.append(node)

    @property
    def child_count(self) -> int:
        return len(self.children)

    def iter_children(self) -> tuple["RTLNode", ...]:
        return tuple(self.children)
