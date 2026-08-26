"""
Focused Unit Tests for TypeResolver edge cases.
"""

import pytest
from app.semantics.type_checking.type_resolver import TypeResolver
from app.ast.expression import LiteralExpression


def test_type_resolver_evaluate_bound_edge_cases():
    resolver = TypeResolver()

    # 1. expression is None (Line 197)
    assert resolver._evaluate_bound(None) is None

    # 2. value is not a valid integer string (Lines 215-221)
    invalid_lit = LiteralExpression(value="not_a_number")
    assert resolver._evaluate_bound(invalid_lit) is None

    # 3. Valid decimal integer literal string
    dec_lit = LiteralExpression(value="16")
    assert resolver._evaluate_bound(dec_lit) == 16

    # 4. Valid hex integer literal string
    hex_lit = LiteralExpression(value="0x10")
    assert resolver._evaluate_bound(hex_lit) == 16
