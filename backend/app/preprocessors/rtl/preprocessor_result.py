"""
Output produced by the RTL preprocessor.
"""

from dataclasses import dataclass

from app.engines.diagnostics.diagnostic import Diagnostic


@dataclass(frozen=True, slots=True)
class RTLPreprocessorResult:

    source: str

    diagnostics: tuple[Diagnostic, ...]

    @property
    def successful(self) -> bool:

        return len(self.diagnostics) == 0
