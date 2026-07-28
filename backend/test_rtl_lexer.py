from app.domain.rtl_tokens import RTLTokenType
from app.parsers.rtl.lexer import RTLLexer


def test_empty_source_produces_only_eof():
    lexer = RTLLexer()

    result = lexer.tokenize("")

    assert result.successful
    assert len(result.tokens) == 1
    assert result.tokens[0].token_type == RTLTokenType.END_OF_FILE


def test_whitespace_only_source_produces_only_eof():
    lexer = RTLLexer()

    result = lexer.tokenize("   \n\t   ")

    assert result.successful
    assert len(result.tokens) == 1
    assert result.tokens[0].token_type == RTLTokenType.END_OF_FILE
