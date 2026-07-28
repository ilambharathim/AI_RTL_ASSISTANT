"""
Factory helpers for deterministic lexer diagnostics.
"""

from app.engines.diagnostics.diagnostic import Diagnostic
from app.engines.diagnostics.diagnostic_severity import (
    DiagnosticSeverity,
)
from app.shared.source_location import SourceLocation


class LexerDiagnosticFactory:
    """
    Creates deterministic lexer diagnostics.
    """

    @staticmethod
    def invalid_based_literal(
        location: SourceLocation,
    ) -> Diagnostic:

        return Diagnostic(
            code="LEX001",
            message="Invalid based numeric literal.",
            severity=DiagnosticSeverity.ERROR,
            stage="LEXER",
            line=location.line,
            column=location.column,
        )

    @staticmethod
    def unterminated_string(
        location: SourceLocation,
    ) -> Diagnostic:

        return Diagnostic(
            code="LEX002",
            message="Unterminated string literal.",
            severity=DiagnosticSeverity.ERROR,
            stage="LEXER",
            line=location.line,
            column=location.column,
        )

    @staticmethod
    def unterminated_block_comment(
        location: SourceLocation,
    ) -> Diagnostic:

        return Diagnostic(
            code="LEX003",
            message="Unterminated block comment.",
            severity=DiagnosticSeverity.ERROR,
            stage="LEXER",
            line=location.line,
            column=location.column,
        )

    @staticmethod
    def unknown_character(
        character: str,
        location: SourceLocation,
    ) -> Diagnostic:

        return Diagnostic(
            code="LEX004",
            message=f"Unknown character: {character!r}",
            severity=DiagnosticSeverity.ERROR,
            stage="LEXER",
            line=location.line,
            column=location.column,
        )
