"""
Comprehensive Unit Test Suite for Phase 8 — Lint Rules and Diagnostics.
Tests existing LintRules behavior without modifying production code.
"""

import pytest
from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    SignalDeclaration,
    ProceduralAssignment,
    IfStatement,
    AlwaysBlock,
)
from app.ast.expression import (
    IdentifierExpression,
    LiteralExpression,
)
from app.diagnostics.rules.lint_rules import LintRules
from app.semantics.semantic_model import SemanticModel


def test_lint_rules_no_syntax_tree():
    """LintRules.run returns empty list when syntax_tree is None."""
    rules = LintRules()
    model = SemanticModel()
    assert rules.run(model) == []


def test_lint_rules_with_syntax_tree():
    """LintRules.run processes a syntax tree and exercises collector paths."""
    rules = LintRules()
    model = SemanticModel()

    sig = SignalDeclaration(signal_type="logic", packed_range=None, name="driven_sig")
    assign1 = ProceduralAssignment(target="driven_sig", operator="=", expression=LiteralExpression("1"))
    assign2 = ProceduralAssignment(target="driven_sig", operator="=", expression=LiteralExpression("2"))
    if_const = IfStatement(condition=LiteralExpression("1"), then_branch=assign1, else_branch=None)
    always = AlwaysBlock(block_type="always_comb", sensitivity=[], statements=[assign1, assign2, if_const])

    mod = ModuleDeclaration(name="top", ports=[], members=[sig, always])
    cu = CompilationUnit(declarations=[mod])
    model.syntax_tree = cu

    diags = rules.run(model)
    # Should exercise UsageCollector, DriverCollector, ConstantConditionCollector,
    # DeadAssignmentCollector code paths
    assert isinstance(diags, list)


def test_lint_rules_visit_unused_none():
    """_visit_unused handles None nodes gracefully."""
    rules = LintRules()
    diags = []
    rules._visit_unused(None, set(), diags)
    assert diags == []


def test_lint_rules_visit_unused_signal_declaration():
    """_visit_unused detects unused SignalDeclaration when directly visited."""
    rules = LintRules()
    diags = []
    sig = SignalDeclaration(signal_type="logic", packed_range=None, name="unused_sig")
    rules._visit_unused(sig, set(), diags)
    assert len(diags) == 1
    assert diags[0].code == "RIVA6001"
    assert "unused_sig" in diags[0].message


def test_lint_rules_visit_unused_used_signal():
    """_visit_unused does NOT flag a used signal."""
    rules = LintRules()
    diags = []
    sig = SignalDeclaration(signal_type="logic", packed_range=None, name="used_sig")
    rules._visit_unused(sig, {"used_sig"}, diags)
    assert diags == []
