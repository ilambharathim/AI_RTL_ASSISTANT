"""
Focused Unit Tests for Phase 8 — Assignment Compatibility Checker.
Tests lookup fallback order (semantic_types, symbols, legacy types), _get_width with object vs dict vs None, and early return branches in _check_assignment.
Tests equal widths, widening, narrowing, scalar/vector, and diagnostic outputs.
"""

import pytest
from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    ProceduralAssignment,
)
from app.ast.expression import IdentifierExpression, LiteralExpression, BinaryExpression
from app.semantics.passes.assignment_compatibility_checker import AssignmentCompatibilityChecker
from app.semantics.semantic_model import SemanticModel


def test_assignment_compatibility_lookup_types_and_get_width():
    checker = AssignmentCompatibilityChecker()
    model = SemanticModel()

    # 1. semantic_types lookup
    class DummySemanticType:
        width = 16

    model.semantic_types["sig_sem"] = DummySemanticType()
    assert checker._lookup_target_type("sig_sem", model) is model.semantic_types["sig_sem"]
    assert checker._get_width(DummySemanticType()) == 16

    # 2. symbols lookup
    model.symbols["sig_sym"] = {"width": 8}
    assert checker._lookup_target_type("sig_sym", model) == {"width": 8}

    # 3. _get_width edge cases
    assert checker._get_width(None) is None
    assert checker._get_width("invalid_string_type") is None


def test_assignment_compatibility_check_assignment_null_branches():
    checker = AssignmentCompatibilityChecker()
    model = SemanticModel()

    # Case A: lhs_type is None
    assign_unknown = ProceduralAssignment(target="unknown_target", operator="=", expression=LiteralExpression("1"))
    checker._check_assignment(assign_unknown, model)

    # Case B: lhs_width is None
    model.types["target_no_width"] = {}
    assign_no_width = ProceduralAssignment(target="target_no_width", operator="=", expression=LiteralExpression("1"))
    checker._check_assignment(assign_no_width, model)

    # Case C: rhs_type is None
    model.types["target_ok"] = {"width": 8}
    assign_rhs_unknown = ProceduralAssignment(target="target_ok", operator="=", expression=IdentifierExpression("unknown_rhs"))
    checker._check_assignment(assign_rhs_unknown, model)

    # Case D: rhs_width is None
    original_infer = checker.expression_type_checker.infer
    try:
        checker.expression_type_checker.infer = lambda expr, m: {}  # dict without width
        assign_rhs_no_width = ProceduralAssignment(target="target_ok", operator="=", expression=LiteralExpression("1"))
        checker._check_assignment(assign_rhs_no_width, model)
    finally:
        checker.expression_type_checker.infer = original_infer


def test_assignment_compatibility_width_variations_and_diagnostics():
    checker = AssignmentCompatibilityChecker()

    # 1. Equal widths (scalar to scalar 1==1)
    model1 = SemanticModel()
    model1.types["a"] = {"width": 1}
    model1.types["b"] = {"width": 1}
    assign1 = ProceduralAssignment(target="a", operator="=", expression=IdentifierExpression("b"))
    checker.check(CompilationUnit(declarations=[ModuleDeclaration(name="top", ports=[], members=[assign1])]), model1)
    assert len(model1.diagnostics) == 0

    # 2. Narrowing (vector 8-bit LHS <- vector 16-bit RHS named)
    model2 = SemanticModel()
    model2.types["a"] = {"width": 8}
    model2.types["b"] = {"width": 16}
    assign2 = ProceduralAssignment(target="a", operator="=", expression=IdentifierExpression("b"))
    checker.check(CompilationUnit(declarations=[ModuleDeclaration(name="top", ports=[], members=[assign2])]), model2)
    assert len(model2.diagnostics) == 1
    assert "Width mismatch: a (8 bits) <- b (16 bits)" in model2.diagnostics[0].message

    # 3. Widening (vector 64-bit LHS <- binary expression RHS without name)
    model3 = SemanticModel()
    model3.types["a"] = {"width": 64}
    model3.types["b"] = {"width": 32}
    model3.types["c"] = {"width": 32}
    bin_expr = BinaryExpression(left=IdentifierExpression("b"), operator="+", right=IdentifierExpression("c"))
    assign3 = ProceduralAssignment(target="a", operator="=", expression=bin_expr)
    checker.check(CompilationUnit(declarations=[ModuleDeclaration(name="top", ports=[], members=[assign3])]), model3)
    assert len(model3.diagnostics) == 1
    assert "Width mismatch: a (64 bits) <- 32 bits" in model3.diagnostics[0].message
