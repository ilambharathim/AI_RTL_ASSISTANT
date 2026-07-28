from app.domain.rtl_tokens import RTLToken
from app.domain.rtl_tokens import RTLTokenType
from app.engines.diagnostics.diagnostic_factory import LexerDiagnosticFactory
from app.parsers.rtl.lexer_result import RTLLexerResult
from app.shared.source_location import SourceLocation

location = SourceLocation(
    line=1,
    column=1,
)

token = RTLToken(
    token_type=RTLTokenType.END_OF_FILE,
    value="",
    source_location=location,
)

result = RTLLexerResult(
    tokens=(token,),
    diagnostics=(),
)

assert result.successful
assert not result.has_errors

diagnostic = LexerDiagnosticFactory.invalid_based_literal(
    location,
)

result = RTLLexerResult(
    tokens=(token,),
    diagnostics=(diagnostic,),
)

assert result.has_errors
assert not result.successful

print("LexerResult infrastructure test passed.")
