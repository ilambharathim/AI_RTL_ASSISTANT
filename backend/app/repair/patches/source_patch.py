"""
Source Patch.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class SourcePatch:

    operation: str

    line: int

    column: int

    text: str
