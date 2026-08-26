"""
Parser result object.
"""

from dataclasses import dataclass

from app.engines.diagnostics.diagnostic import Diagnostic


@dataclass(frozen=True, slots=True)
class RTLParserResult:

    syntax_tree: object | None

    rtl_ast: object | None

    diagnostics: tuple[Diagnostic, ...]

    @property
    def successful(self) -> bool:

        return len(self.diagnostics) == 0
