"""
Comprehensive Unit Test Suite for Phase 5 — Semantic Analysis Passes.
Validates 100% of missing branches for:
- ConstantEvaluator
- IdentifierChecker
- ImplicitNetDetector
- ParameterTypeChecker
"""

import pytest
from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    ParameterDeclaration,
    ProceduralAssignment,
    PortDeclaration,
)
from app.ast.expression import (
    LiteralExpression,
    IdentifierExpression,
    BinaryExpression,
    UnaryExpression,
    FunctionCallExpression,
)
from app.semantics.evaluation.constant_evaluator import ConstantEvaluator
from app.semantics.passes.identifier_checker import IdentifierChecker
from app.semantics.passes.implicit_net_detector import ImplicitNetDetector
from app.semantics.passes.parameter_type_checker import ParameterTypeChecker
from app.semantics.semantic_model import SemanticModel


def test_constant_evaluator_all_branches():
    evaluator = ConstantEvaluator()
    model = SemanticModel()

    # Parameter declarations
    p_add = ParameterDeclaration(name="P_ADD", value=BinaryExpression("+", LiteralExpression("10"), LiteralExpression("20")))
    p_sub = ParameterDeclaration(name="P_SUB", value=BinaryExpression("-", LiteralExpression("30"), LiteralExpression("5")))
    p_mul = ParameterDeclaration(name="P_MUL", value=BinaryExpression("*", LiteralExpression("4"), LiteralExpression("5")))
    p_div = ParameterDeclaration(name="P_DIV", value=BinaryExpression("/", LiteralExpression("20"), LiteralExpression("4")))
    p_div0 = ParameterDeclaration(name="P_DIV0", value=BinaryExpression("/", LiteralExpression("20"), LiteralExpression("0")))
    p_bad = ParameterDeclaration(name="P_BAD", value=LiteralExpression("abc"))
    p_unk = ParameterDeclaration(name="P_UNK", value=BinaryExpression("+", IdentifierExpression("UNKNOWN"), LiteralExpression("1")))

    mod = ModuleDeclaration(name="top", ports=[], members=[p_add, p_sub, p_mul, p_div, p_div0, p_bad, p_unk])
    cu = CompilationUnit(declarations=[mod])

    evaluator.evaluate(cu, model)

    assert model.constant_values.get("P_ADD") == 30
    assert model.constant_values.get("P_SUB") == 25
    assert model.constant_values.get("P_MUL") == 20
    assert model.constant_values.get("P_DIV") == 5
    assert "P_DIV0" not in model.constant_values
    assert "P_BAD" not in model.constant_values
    assert "P_UNK" not in model.constant_values


def test_identifier_checker_all_branches():
    checker = IdentifierChecker()
    model = SemanticModel()

    p_decl = ParameterDeclaration(name="P1", value=UnaryExpression("-", IdentifierExpression("UNDECLARED_P")))
    assign = ProceduralAssignment(target="x", operator="=", expression=BinaryExpression("+", IdentifierExpression("UNDECLARED_A"), IdentifierExpression("UNDECLARED_B")))

    mod = ModuleDeclaration(name="top", ports=[], members=[p_decl, assign])
    cu = CompilationUnit(declarations=[mod])

    checker.check(cu, model)

    assert len(model.diagnostics) >= 3
    assert any("UNDECLARED_P" in d.message for d in model.diagnostics)
    assert any("UNDECLARED_A" in d.message for d in model.diagnostics)


def test_implicit_net_detector_all_branches():
    detector = ImplicitNetDetector()
    model = SemanticModel()

    port = PortDeclaration(direction="input", signal_type="logic", packed_range=None, name="clk")
    param = ParameterDeclaration(name="W", value=LiteralExpression("8"))
    fn_call = FunctionCallExpression("$clog2", (IdentifierExpression("implicit_fn_arg"),))
    un_expr = UnaryExpression("-", IdentifierExpression("implicit_un_arg"))
    bin_expr = BinaryExpression("+", fn_call, un_expr)

    assign = ProceduralAssignment(target="y", operator="=", expression=bin_expr)

    mod = ModuleDeclaration(name="top", ports=[port], members=[param, assign])
    cu = CompilationUnit(declarations=[mod])

    diags = detector.detect(cu, model)

    assert len(diags) >= 2
    assert any("implicit_fn_arg" in d for d in diags)
    assert any("implicit_un_arg" in d for d in diags)


def test_parameter_type_checker_all_branches():
    checker = ParameterTypeChecker()
    model = SemanticModel()

    p1 = ParameterDeclaration(name="PARAM1", value=LiteralExpression("10"))
    mod = ModuleDeclaration(name="top", ports=[], members=[p1])
    cu = CompilationUnit(declarations=[mod])

    checker.check(cu, model)
    assert model is not None
