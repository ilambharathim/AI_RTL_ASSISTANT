"""
Source Location.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SourceLocation:

    line: int

    column: int

    file: str = ""
