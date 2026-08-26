"""
Focused Unit Tests for SemanticModel helper methods.
"""

import pytest
from app.semantics.semantic_model import SemanticModel


def test_semantic_model_constant_values():
    model = SemanticModel()
    model.set_constant_value("WIDTH", 32)
    assert model.get_constant_value("WIDTH") == 32
    assert model.get_constant_value("UNKNOWN") is None


def test_semantic_model_semantic_types():
    model = SemanticModel()
    model.set_semantic_type("clk", "logic")
    assert model.get_semantic_type("clk") == "logic"
    assert model.get_semantic_type("UNKNOWN") is None
