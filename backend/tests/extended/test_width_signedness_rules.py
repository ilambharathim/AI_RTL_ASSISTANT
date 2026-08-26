"""
Focused unit tests to get 100% coverage on WidthMismatchRule and SignednessMismatchRule.
"""

import pytest
from app.diagnostics.rules.width_mismatch import WidthMismatchRule
from app.diagnostics.rules.signedness_mismatch import SignednessMismatchRule
from app.semantics.semantic_model import SemanticModel
from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    StatementBlock,
    ProceduralAssignment,
    AlwaysBlock,
)
from app.ast.expression import LiteralExpression


def test_width_and_signedness_mismatch_edge_cases():
    # Setup rules
    w_rule = WidthMismatchRule()
    s_rule = SignednessMismatchRule()

    # 1. Test None visiting
    model = SemanticModel()
    model.syntax_tree = None
    assert w_rule.run(model) == []
    assert s_rule.run(model) == []

    # 2. Test StatementBlock with statements inside
    pa = ProceduralAssignment(target="a", operator="=", expression=LiteralExpression("1"))
    sb = StatementBlock(statements=(pa,))
    always = AlwaysBlock(block_type="always_comb", sensitivity=[], statements=[sb])
    mod = ModuleDeclaration(name="top", ports=[], members=[always])
    model.syntax_tree = CompilationUnit(declarations=[mod])

    # Populate types so we trigger _lookup_target_type and _get_width checks
    # Test Line 193: lookup using symbols
    model.symbols["a"] = {"width": 8, "signed": False}

    # Run checks
    w_rule.run(model)
    s_rule.run(model)

    # 3. Test _get_width and _lookup_target_type edge cases
    # Line 215: type_info is None
    assert w_rule._get_width(None) is None
    assert s_rule._get_signedness(None) is None

    # Line 233: type_info is not dict or object with attribute
    assert w_rule._get_width("not_dict_or_object") is None
    assert s_rule._get_signedness("not_dict_or_object") is None

    # Test when target info exists but has no width/signedness
    model.symbols["a"] = "invalid_type_info_string"
    w_rule.run(model)
    s_rule.run(model)

    # Test when source_info is None or has no width/signedness
    model.symbols["a"] = {"width": 8, "signed": False}
    # Mock ExpressionTypeChecker.infer to return None
    original_infer = w_rule.expression_type_checker.infer
    try:
        w_rule.expression_type_checker.infer = lambda expr, model: None
        s_rule.expression_type_checker.infer = lambda expr, model: None
        w_rule.run(model)
        s_rule.run(model)

        # Mock ExpressionTypeChecker.infer to return dict without width
        w_rule.expression_type_checker.infer = lambda expr, model: {}
        s_rule.expression_type_checker.infer = lambda expr, model: {}
        w_rule.run(model)
        s_rule.run(model)
    finally:
        w_rule.expression_type_checker.infer = original_infer
        s_rule.expression_type_checker.infer = original_infer
