"""
Factory helpers for constructing immutable diagnostics.

Compiler stages should create diagnostics through these helpers
instead of constructing Diagnostic objects directly.
"""

from app.engines.diagnostics.diagnostic import Diagnostic
from app.engines.diagnostics.diagnostic_severity import DiagnosticSeverity
from app.shared.source_location import SourceLocation


class LexerDiagnosticFactory:
    """
    Factory for deterministic lexer diagnostics.
    """

    STAGE = "LEXER"

    @staticmethod
    def invalid_based_literal(
        location: SourceLocation,
        source_file: str = "",
    ) -> Diagnostic:

        return Diagnostic(
            code="LEX001",
            message="Invalid based numeric literal.",
            severity=DiagnosticSeverity.ERROR,
            stage=LexerDiagnosticFactory.STAGE,
            line=location.line,
            column=location.column,
            source_file=source_file,
        )

    @staticmethod
    def unterminated_string(
        location: SourceLocation,
        source_file: str = "",
    ) -> Diagnostic:

        return Diagnostic(
            code="LEX002",
            message="Unterminated string literal.",
            severity=DiagnosticSeverity.ERROR,
            stage=LexerDiagnosticFactory.STAGE,
            line=location.line,
            column=location.column,
            source_file=source_file,
        )

    @staticmethod
    def unterminated_block_comment(
        location: SourceLocation,
        source_file: str = "",
    ) -> Diagnostic:

        return Diagnostic(
            code="LEX003",
            message="Unterminated block comment.",
            severity=DiagnosticSeverity.ERROR,
            stage=LexerDiagnosticFactory.STAGE,
            line=location.line,
            column=location.column,
            source_file=source_file,
        )

    @staticmethod
    def unsupported_character(
        character: str,
        location: SourceLocation,
        source_file: str = "",
    ) -> Diagnostic:

        return Diagnostic(
            code="LEX004",
            message=f"Unsupported character: {character!r}",
            severity=DiagnosticSeverity.ERROR,
            stage=LexerDiagnosticFactory.STAGE,
            line=location.line,
            column=location.column,
            source_file=source_file,
        )
