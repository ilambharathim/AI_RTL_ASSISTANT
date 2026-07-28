from dataclasses import dataclass

from app.domain.rtl_tokens import RTLToken
from app.engines.diagnostics.diagnostic import Diagnostic
from app.engines.diagnostics.diagnostic_severity import DiagnosticSeverity


@dataclass(slots=True, frozen=True)
class RTLLexerResult:
    """
    Immutable result produced by the deterministic RTL lexer.
    """

    tokens: tuple[RTLToken, ...]
    diagnostics: tuple[Diagnostic, ...]

    def __post_init__(self) -> None:

        if not isinstance(self.tokens, tuple):
            raise TypeError("tokens must be a tuple.")

        if not all(
            isinstance(token, RTLToken)
            for token in self.tokens
        ):
            raise TypeError(
                "tokens must contain only RTLToken objects."
            )

        if not isinstance(self.diagnostics, tuple):
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
        return not self.has_errors

    @property
    def has_errors(self) -> bool:
        return any(
            diagnostic.severity == DiagnosticSeverity.ERROR
            for diagnostic in self.diagnostics
        )

    @property
    def has_warnings(self) -> bool:
        return any(
            diagnostic.severity == DiagnosticSeverity.WARNING
            for diagnostic in self.diagnostics
        )
