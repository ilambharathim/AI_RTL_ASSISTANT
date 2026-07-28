from app.engines.diagnostics.diagnostic_factory import LexerDiagnosticFactory
from app.engines.diagnostics.diagnostic_severity import DiagnosticSeverity
from app.shared.source_location import SourceLocation

location = SourceLocation(
    line=12,
    column=7,
)

diagnostic = LexerDiagnosticFactory.invalid_based_literal(
    location,
)

assert diagnostic.code == "LEX001"
assert diagnostic.severity == DiagnosticSeverity.ERROR
assert diagnostic.line == 12
assert diagnostic.column == 7
assert diagnostic.stage == "LEXER"

print("Diagnostic factory test passed.")
