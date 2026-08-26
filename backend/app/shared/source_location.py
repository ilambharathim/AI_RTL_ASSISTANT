"""
Immutable source-location value object shared across RIVA stages.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SourceLocation:
    """
    Identifies a location in an input artifact.

    Line and column use zero when an exact source coordinate is unavailable.
    Source-backed locations should use one-based line and column values.
    """

    source_file: str = ""
    line: int = 0
    column: int = 0

    def __init__(
        self,
        source_file: str = "",
        line: int = 0,
        column: int = 0,
        file: str = "",
    ) -> None:
        sf = source_file if source_file else file
        object.__setattr__(self, "source_file", sf)
        object.__setattr__(self, "line", line)
        object.__setattr__(self, "column", column)
        self.__post_init__()

    @property
    def file(self) -> str:
        return self.source_file

    def __post_init__(self) -> None:
        if not isinstance(self.source_file, str):
            raise TypeError("source_file must be a string.")

        if type(self.line) is not int or self.line < 0:
            raise ValueError(
                "line must be an integer greater than or equal to 0."
            )

        if type(self.column) is not int or self.column < 0:
            raise ValueError(
                "column must be an integer greater than or equal to 0."
            )

    @property
    def is_known(self) -> bool:
        """
        Return whether any source-location information is available.
        """

        return bool(self.source_file) or self.line > 0 or self.column > 0

    def __str__(self) -> str:
        """
        Return a stable compiler-style location string.
        """

        location = self.source_file or "<memory>"

        if self.line > 0:
            location += f":{self.line}"

        if self.column > 0:
            location += f":{self.column}"

        return location
