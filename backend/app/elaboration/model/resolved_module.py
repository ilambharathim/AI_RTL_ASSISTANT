"""
Resolved Module.

Canonical representation of a module after elaboration.
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class ResolvedModule:

    name: str

    declaration: object

    parameters: dict = field(
        default_factory=dict,
    )

    ports: dict = field(
        default_factory=dict,
    )

    signals: dict = field(
        default_factory=dict,
    )

    instances: dict = field(
        default_factory=dict,
    )

    cfg: object | None = None

    rtl_graph: object | None = None

    dataflow: object | None = None
