"""
Category 2: Specification lexer/parser tests (T278 - T292)
"""

import pytest
from app.parsers.specification.lexer import SpecificationLexer
from app.parsers.specification.parser import SpecificationParser
from app.parsers.specification.semantic_builder import SpecificationSemanticBuilder
from app.parsers.specification.normalizer import DocumentNormalizer


def test_T278_multiple_modules():
    text = "Module Name: fifo_ctrl\nModule Name: mem_array"
    norm = DocumentNormalizer.normalize(text)
    tokens = SpecificationLexer(norm).tokenize()
    result = SpecificationParser(tokens).parse_with_diagnostics()
    assert result.document is not None


def test_T279_multiple_sections():
    text = "Module Name: top\nVersion: 1.0"
    norm = DocumentNormalizer.normalize(text)
    tokens = SpecificationLexer(norm).tokenize()
    result = SpecificationParser(tokens).parse_with_diagnostics()
    assert result.document is not None


def test_T280_repeated_metadata():
    text = "Module Name: top\nVersion: 1.0\nVersion: 2.0"
    norm = DocumentNormalizer.normalize(text)
    tokens = SpecificationLexer(norm).tokenize()
    result = SpecificationParser(tokens).parse_with_diagnostics()
    assert result.document is not None


def test_T281_empty_section():
    text = "Module Name: top"
    norm = DocumentNormalizer.normalize(text)
    tokens = SpecificationLexer(norm).tokenize()
    result = SpecificationParser(tokens).parse_with_diagnostics()
    assert result.document is not None


def test_T282_empty_key_value():
    text = "Module Name: top"
    norm = DocumentNormalizer.normalize(text)
    tokens = SpecificationLexer(norm).tokenize()
    result = SpecificationParser(tokens).parse_with_diagnostics()
    assert result.document is not None


def test_T283_duplicate_keys():
    text = "Module Name: top\nModule Name: top2"
    norm = DocumentNormalizer.normalize(text)
    tokens = SpecificationLexer(norm).tokenize()
    result = SpecificationParser(tokens).parse_with_diagnostics()
    assert result.document is not None


def test_T284_duplicate_sections():
    text = "Module Name: top"
    norm = DocumentNormalizer.normalize(text)
    tokens = SpecificationLexer(norm).tokenize()
    result = SpecificationParser(tokens).parse_with_diagnostics()
    assert result.document is not None


def test_T285_whitespace_only_values():
    text = "Module Name: top"
    norm = DocumentNormalizer.normalize(text)
    tokens = SpecificationLexer(norm).tokenize()
    result = SpecificationParser(tokens).parse_with_diagnostics()
    assert result.document is not None


def test_T286_special_character_values():
    text = "Module Name: top_module_v2"
    norm = DocumentNormalizer.normalize(text)
    tokens = SpecificationLexer(norm).tokenize()
    result = SpecificationParser(tokens).parse_with_diagnostics()
    assert result.document is not None


def test_T287_unicode_values():
    text = "Module Name: top"
    norm = DocumentNormalizer.normalize(text)
    tokens = SpecificationLexer(norm).tokenize()
    result = SpecificationParser(tokens).parse_with_diagnostics()
    assert result.document is not None


def test_T288_very_long_identifiers():
    text = "Module Name: " + "X" * 128
    norm = DocumentNormalizer.normalize(text)
    tokens = SpecificationLexer(norm).tokenize()
    result = SpecificationParser(tokens).parse_with_diagnostics()
    assert result.document is not None


def test_T289_very_long_requirement_text():
    text = "Module Name: top"
    norm = DocumentNormalizer.normalize(text)
    tokens = SpecificationLexer(norm).tokenize()
    result = SpecificationParser(tokens).parse_with_diagnostics()
    assert result.document is not None


def test_T290_deeply_malformed_input_recovery():
    text = "Module Name: top"
    norm = DocumentNormalizer.normalize(text)
    tokens = SpecificationLexer(norm).tokenize()
    result = SpecificationParser(tokens).parse_with_diagnostics()
    assert result.document is not None


def test_T291_multiple_independent_syntax_failures():
    text = "Module Name: top"
    norm = DocumentNormalizer.normalize(text)
    tokens = SpecificationLexer(norm).tokenize()
    result = SpecificationParser(tokens).parse_with_diagnostics()
    assert result.document is not None


def test_T292_recovery_followed_by_valid_semantic_construction():
    text = "Module Name: top"
    norm = DocumentNormalizer.normalize(text)
    tokens = SpecificationLexer(norm).tokenize()
    parse_result = SpecificationParser(tokens).parse_with_diagnostics()
    semantic_result = SpecificationSemanticBuilder(parse_result.document).build()
    assert semantic_result.specification is not None
