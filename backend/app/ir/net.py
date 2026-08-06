"""
Net IR node.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Net:

    port: str

    signal: str | None

    constant: object | None = None

