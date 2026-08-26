"""
Focused Unit Tests for Phase 10 — Secondary Gaps.
Tests GenerateSubstituter and ParameterTypeChecker.
"""

import pytest
from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    ParameterDeclaration,
)
from app.ast.expression import (
    IdentifierExpression,
    BinaryExpression,
    UnaryExpression,
    LiteralExpression,
)
from app.elaboration.utils.generate_substituter import GenerateSubstituter
from app.semantics.passes.parameter_type_checker import ParameterTypeChecker
from app.semantics.semantic_model import SemanticModel


def test_generate_substituter_coverage():
    # Substitute variable "i" with 5 inside a nested node tree
    ident_i = IdentifierExpression("i")
    ident_x = IdentifierExpression("x")
    un_expr = UnaryExpression(operator="!", operand=ident_i)
    bin_expr = BinaryExpression(left=ident_x, operator="+", right=un_expr)

    res = GenerateSubstituter.substitute(bin_expr, "i", 5)
    # ident_i should be converted to LiteralExpression("5")
    assert un_expr.operand.name == "5"
    assert un_expr.operand.kind == "LiteralExpression"

    # Test None node
    assert GenerateSubstituter.substitute(None, "i", 0) is None

    # Test object whose getattr raises exception or has tuple attributes
    class FaultyObj:
        __slots__ = ("faulty_attr", "valid_tuple")

        def __getattribute__(self, item):
            if item == "faulty_attr":
                raise ValueError("error reading attr")
            return super().__getattribute__(item)

    obj = FaultyObj()
    obj.valid_tuple = (IdentifierExpression("i"),)
    GenerateSubstituter.substitute(obj, "i", 10)
    assert obj.valid_tuple[0].name == "10"


def test_parameter_type_checker_coverage():
    checker = ParameterTypeChecker()
    model = SemanticModel()

    # 1. Parameter with BinaryExpression referencing types and constant_values
    model.types["PARAM_A"] = {"width": 32}
    model.constant_values["PARAM_B"] = 100

    # parameter P = PARAM_A + (-PARAM_B);
    param_val = BinaryExpression(
        left=IdentifierExpression("PARAM_A"),
        operator="+",
        right=UnaryExpression(operator="-", operand=IdentifierExpression("PARAM_B")),
    )
    param_decl = ParameterDeclaration(name="P", value=param_val)
    mod_decl = ModuleDeclaration(name="top", ports=[], members=[param_decl])
    cu = CompilationUnit(declarations=[mod_decl])

    checker.check(cu, model)
    assert len(model.diagnostics) == 0

    # 2. Parameter referencing undeclared identifier
    param_val_bad = IdentifierExpression("UNDECLARED_ID")
    param_decl_bad = ParameterDeclaration(name="P_BAD", value=param_val_bad)
    mod_bad = ModuleDeclaration(name="top2", ports=[], members=[param_decl_bad])

    checker.check(mod_bad, model)
    assert len(model.diagnostics) == 1
    assert "UNDECLARED_ID" in model.diagnostics[0].message
