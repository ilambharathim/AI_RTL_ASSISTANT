"""
Focused Unit Tests for Phase 2 — Legacy RTL AST Adapter.
Tests all missing conversion paths, expression nodes, unary operators, function calls, and range parsing.
"""

import pytest
from app.ast.compilation_unit import CompilationUnit
from app.ast.module_declaration import ModuleDeclaration
from app.ast.generate_block import GenerateBlock
from app.ast.generate_for import GenerateFor
from app.ast.generate_if import GenerateIf
from app.ast.expression import (
    UnaryExpression,
    FunctionCallExpression,
    LiteralExpression,
)
from app.parsers.rtl.adapters.legacy_to_rtl_ast import LegacyToRTLASTAdapter
from app.domain.rtl_ast import GenerateNode, RTLCompilationUnit


def test_legacy_to_rtl_ast_invalid_input():
    with pytest.raises(TypeError, match="syntax_tree must be a legacy CompilationUnit"):
        LegacyToRTLASTAdapter.convert("not_a_compilation_unit")


def test_legacy_to_rtl_ast_generate_block_and_unknown_members():
    class UnknownMember:
        pass

    mod = ModuleDeclaration(
        name="top",
        ports=(),
        members=(
            GenerateBlock(members=()),
            GenerateFor("i", LiteralExpression("0"), LiteralExpression("i < 4"), LiteralExpression("i+1"), ()),
            GenerateIf(LiteralExpression("1"), ()),
            UnknownMember(),
        ),
    )
    cu = CompilationUnit(declarations=(mod,))

    rtl_cu = LegacyToRTLASTAdapter.convert(cu)
    assert isinstance(rtl_cu, RTLCompilationUnit)
    assert len(rtl_cu.modules) == 1
    top_mod = rtl_cu.modules[0]

    # Check generate nodes
    gen_nodes = [m for m in top_mod.members if isinstance(m, GenerateNode)]
    assert len(gen_nodes) == 3
    assert any(g.generate_type == "block" for g in gen_nodes)
    assert any(g.generate_type == "for" for g in gen_nodes)
    assert any(g.generate_type == "if" for g in gen_nodes)


def test_legacy_to_rtl_ast_expression_text_rendering():
    # None
    assert LegacyToRTLASTAdapter._expression_text(None) == ""

    # Raw string
    assert LegacyToRTLASTAdapter._expression_text("my_sig") == "my_sig"

    # Unary expression (operator + operand)
    unary = UnaryExpression(operator="!", operand=LiteralExpression("0"))
    assert LegacyToRTLASTAdapter._expression_text(unary) == "!0"

    # Function Call
    sys_call = FunctionCallExpression(
        function_name="$clog2",
        arguments=(LiteralExpression("16"), LiteralExpression("2")),
    )
    assert LegacyToRTLASTAdapter._expression_text(sys_call) == "$clog2(16, 2)"


def test_legacy_to_rtl_ast_literal_int_and_packed_range():
    # packed_range is None
    assert LegacyToRTLASTAdapter._packed_range_width(None) == 1

    # node is int directly
    assert LegacyToRTLASTAdapter._literal_int(5) == 5

    # node is string causing ValueError
    invalid_lit = LiteralExpression(value="not_a_number")
    assert LegacyToRTLASTAdapter._literal_int(invalid_lit) is None
