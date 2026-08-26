"""
Focused Unit Tests for StringReader.
Tests standard strings, empty strings, escaped characters (\\n, \\t, \\\\, \\"), unknown escape sequences, and unterminated strings.
"""

import pytest
from app.parsers.rtl.character_stream import CharacterStream
from app.parsers.rtl.readers.string_reader import StringReader
from app.domain.rtl_tokens import RTLTokenType


def test_string_reader_standard_and_escapes():
    diagnostics = []

    # Standard string with escapes: "hello\nworld\ttest\\\""
    stream = CharacterStream(source='"hello\\nworld\\ttest\\\\\\""')
    token = StringReader.read(stream, diagnostics)

    assert token.token_type == RTLTokenType.STRING
    assert token.value == 'hello\nworld\ttest\\"'
    assert len(diagnostics) == 0


def test_string_reader_empty_string():
    diagnostics = []
    stream = CharacterStream(source='""')
    token = StringReader.read(stream, diagnostics)

    assert token.token_type == RTLTokenType.STRING
    assert token.value == ""
    assert len(diagnostics) == 0


def test_string_reader_unknown_escape():
    diagnostics = []
    # "hello\xworld"
    stream = CharacterStream(source='"hello\\xworld"')
    token = StringReader.read(stream, diagnostics)

    assert token.token_type == RTLTokenType.STRING
    assert token.value == "helloxworld"
    assert len(diagnostics) == 1
    assert "unknown escape" in diagnostics[0].message


def test_string_reader_unterminated_escape_at_eof():
    diagnostics = []
    # "hello\
    stream = CharacterStream(source='"hello\\')
    token = StringReader.read(stream, diagnostics)

    assert token.token_type == RTLTokenType.STRING
    assert token.value == "hello"
    assert len(diagnostics) == 2  # unterminated escape sequence + unterminated string literal


def test_string_reader_unterminated_string():
    diagnostics = []
    # "hello world
    stream = CharacterStream(source='"hello world')
    token = StringReader.read(stream, diagnostics)

    assert token.token_type == RTLTokenType.STRING
    assert token.value == "hello world"
    assert len(diagnostics) == 1
    assert "Unterminated string literal" in diagnostics[0].message
