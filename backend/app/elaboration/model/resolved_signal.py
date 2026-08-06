"""
Resolved signal.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class ResolvedSignal:

    port_name: str

    expression: object = None

    symbol: object = None

