from dataclasses import dataclass

from app.domain.rtl_ast import RTLCompilationUnit
from app.engines.diagnostics.diagnostic import Diagnostic


@dataclass(slots=True, frozen=True)
class RTLParseResult:
    """
    Immutable result produced by the deterministic RTL parser.
    """

    compilation_unit: RTLCompilationUnit
    diagnostics: tuple[Diagnostic, ...]

    def __post_init__(self) -> None:
        if not isinstance(
            self.compilation_unit,
            RTLCompilationUnit,
        ):
            raise TypeError(
                "compilation_unit must be an RTLCompilationUnit."
            )

        if not isinstance(
            self.diagnostics,
            tuple,
        ):
            raise TypeError(
                "diagnostics must be a tuple."
            )

        if not all(
            isinstance(diagnostic, Diagnostic)
            for diagnostic in self.diagnostics
        ):
            raise TypeError(
                "diagnostics must contain only Diagnostic objects."
            )

    @property
    def successful(self) -> bool:
        return len(self.diagnostics) == 0
