"""
Priority 3 — Small Cleanup Coverage.
Tests meaningful methods on base Type and TypeResolver edge cases.
"""

import pytest
from app.semantics.types.base.type import Type


def test_base_type_str():
    t = Type(name="logic")
    assert str(t) == "logic"


def test_base_type_repr():
    t = Type(name="reg")
    assert repr(t) == "Type(name='reg')"


def test_base_type_equality():
    t1 = Type(name="logic")
    t2 = Type(name="logic")
    t3 = Type(name="wire")
    assert t1 == t2
    assert t1 != t3
