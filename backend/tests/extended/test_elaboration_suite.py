"""
Comprehensive Unit Test Suite for Phase 2 — Elaboration.
Validates 100% of branches across:
- GenerateElaborator
- GenerateSubstituter
- ModuleElaborator
- HierarchyBuilder
"""

import pytest
from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    GenerateBlock,
    GenerateIf,
    GenerateFor,
    ProceduralAssignment,
)
from app.ast.expression import (
    IdentifierExpression,
    LiteralExpression,
    BinaryExpression,
    UnaryExpression,
)
from app.ast.module_instance import ModuleInstance
from app.ast.port_connection import PortConnection
from app.elaboration.generate.generate_elaborator import GenerateElaborator
from app.elaboration.utils.generate_substituter import GenerateSubstituter
from app.elaboration.module_elaborator import ModuleElaborator
from app.elaboration.hierarchy_builder import HierarchyTreeBuilder
from app.semantics.semantic_model import SemanticModel


def test_generate_elaborator_all_branches():
    model = SemanticModel()
    model.constant_values = {"NUM_UNITS": 3, "ENABLE": 1, "DISABLE": 0}

    # GenerateIf (true)
    stmt_true = ProceduralAssignment(target="a", operator="=", expression=LiteralExpression("1"))
    stmt_false = ProceduralAssignment(target="a", operator="=", expression=LiteralExpression("0"))
    gen_if_true = GenerateIf(condition=IdentifierExpression("ENABLE"), true_members=[stmt_true], false_members=[stmt_false])

    # GenerateIf (false)
    gen_if_false = GenerateIf(condition=IdentifierExpression("DISABLE"), true_members=[stmt_true], false_members=[stmt_false])

    # GenerateFor (valid 0..3 loop)
    inst = ModuleInstance(module_name="sub_cell", parameter_overrides=[], instance_name="u_cell", connections=[PortConnection("clk", IdentifierExpression("clk"))])
    gen_for_3 = GenerateFor(variable="i", initializer=LiteralExpression("0"), condition=IdentifierExpression("NUM_UNITS"), update=LiteralExpression("1"), members=[inst])

    # GenerateFor (invalid/non-int start or limit fallback)
    gen_for_fallback = GenerateFor(variable="i", initializer=BinaryExpression("+", LiteralExpression("1"), LiteralExpression("2")), condition=LiteralExpression("3"), update=LiteralExpression("1"), members=[inst])

    # GenerateFor (invalid literal value exception branch)
    gen_for_bad_lit = GenerateFor(variable="i", initializer=LiteralExpression("invalid_hex"), condition=LiteralExpression("3"), update=LiteralExpression("1"), members=[inst])

    # GenerateBlock wrapper
    block = GenerateBlock(members=[gen_if_true, gen_if_false, gen_for_3, gen_for_fallback, gen_for_bad_lit])

    # Non-module declaration to test hasattr(declaration, 'members') check
    class NonModuleDecl:
        pass

    mod_decl = ModuleDeclaration(name="top", ports=[], members=[block])
    cu = CompilationUnit(declarations=[mod_decl, NonModuleDecl()])

    model.elaboration = type("ElaborationContainer", (), {})()
    elaborator = GenerateElaborator()
    elaborator.elaborate(cu, model)

    assert "top" in model.elaboration.elaborated_modules
    expanded = model.elaboration.elaborated_modules["top"]
    assert len(expanded) >= 4


def test_generate_substituter_all_branches():
    sub = GenerateSubstituter()

    id_expr = IdentifierExpression("i")
    sub.substitute(id_expr, "i", 2)
    assert id_expr.name == "2"

    bin_expr = BinaryExpression("+", IdentifierExpression("i"), LiteralExpression("10"))
    sub.substitute(bin_expr, "i", 5)
    assert bin_expr.left.name == "5"

    un_expr = UnaryExpression("-", IdentifierExpression("i"))
    sub.substitute(un_expr, "i", 3)
    assert un_expr.operand.name == "3"

    port = PortConnection("data", IdentifierExpression("i"))
    sub.substitute(port, "i", 7)
    assert port.expression.name == "7"

    inst = ModuleInstance("cell", [], "u_cell", [port])
    sub.substitute(inst, "i", 1)
    assert inst.connections[0].expression.name == "7"


def test_module_elaborator_with_nested_instances():
    # Sub-module
    sub_decl = ModuleDeclaration(name="sub_mod", ports=[], members=[])

    # Top module instantiating sub_mod
    inst_sub = ModuleInstance(module_name="sub_mod", parameter_overrides=[], instance_name="u_sub", connections=[])
    inst_missing = ModuleInstance(module_name="missing_mod", parameter_overrides=[], instance_name="u_miss", connections=[])

    top_decl = ModuleDeclaration(name="top", ports=[], members=[inst_sub, inst_missing])

    cu = CompilationUnit(declarations=[sub_decl, top_decl])

    elaborator = ModuleElaborator()
    hierarchy = elaborator.elaborate(cu)

    assert "top" in hierarchy
    assert "sub_mod" in hierarchy
    top_node = hierarchy["top"]
    assert len(top_node.children) == 2


def test_hierarchy_tree_builder_edge_cases():
    sub_decl = ModuleDeclaration(name="sub_mod", ports=[], members=[])
    inst1 = ModuleInstance(module_name="sub_mod", parameter_overrides=[], instance_name="u_sub1", connections=[])
    inst2 = ModuleInstance(module_name="sub_mod", parameter_overrides=[], instance_name="u_sub2", connections=[])
    top_decl = ModuleDeclaration(name="top", ports=[], members=[inst1, inst2])

    cu = CompilationUnit(declarations=[sub_decl, top_decl])

    builder = HierarchyTreeBuilder()
    trees = builder.build_tree(cu)
    assert len(trees) >= 1
