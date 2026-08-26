"""
Focused Unit Tests for PortValidator edge cases and branch coverage.
"""

import pytest
from app.ast import (
    CompilationUnit,
    ModuleDeclaration,
    PortDeclaration,
    SignalDeclaration,
)
from app.ast.module_instance import ModuleInstance
from app.ast.port_connection import PortConnection
from app.ast.expression import IdentifierExpression, LiteralExpression
from app.elaboration.validation.port_validator import PortValidator
from app.semantics.semantic_model import SemanticModel


def test_port_validator_unknown_module_instance_and_non_module_declarations():
    validator = PortValidator()
    model = SemanticModel()

    # Non-module declaration in syntax_tree.declarations
    class DummyOtherDecl:
        pass

    # Module instance instantiating unknown target module
    inst_unknown = ModuleInstance("unknown_mod", (), "u1", ())
    mod_top = ModuleDeclaration(name="top", ports=(), members=(inst_unknown,))

    cu = CompilationUnit(declarations=(DummyOtherDecl(), mod_top))

    diags = validator.validate(cu, model)
    assert len(diags) == 0  # Unknown module instance skips validation (Line 76)


def test_port_validator_connection_expression_without_name_and_unresolved_widths():
    validator = PortValidator()
    model = SemanticModel()

    # Connection expression is LiteralExpression (no name attribute) -> Line 126
    conn_lit = PortConnection(port_name="in_p", expression=LiteralExpression("1"))

    # Connection with unresolved signal width -> Line 142
    conn_unresolved = PortConnection(port_name="out_p", expression=IdentifierExpression("unresolved_sig"))

    inst = ModuleInstance("sub_mod", (), "u_sub", (conn_lit, conn_unresolved))
    sub_decl = ModuleDeclaration(
        name="sub_mod",
        ports=(PortDeclaration(name="in_p", direction="input", signal_type="logic", packed_range=None),
               PortDeclaration(name="out_p", direction="output", signal_type="logic", packed_range=None)),
        members=()
    )
    top_decl = ModuleDeclaration(name="top", ports=(), members=(inst,))

    cu = CompilationUnit(declarations=(sub_decl, top_decl))
    diags = validator.validate(cu, model)

    # Missing ports is 0 because in_p and out_p are connected
    assert len(diags) == 0


def test_port_validator_lookup_width_fallthrough():
    validator = PortValidator()
    model = SemanticModel()

    # 1. semantic_types entry without width attribute (falls through to symbols)
    class DummyTypeNoWidth:
        width = None

    model.semantic_types["sig1"] = DummyTypeNoWidth()

    # 2. symbol entry without width attribute or semantic_type attribute (falls through to types)
    class DummySymbolNoWidth:
        width = None
        semantic_type = None

    model.symbols["sig1"] = DummySymbolNoWidth()
    model.types["sig1"] = {"width": 16}

    assert validator._lookup_width("sig1", model) == 16

    # 3. symbol entry with semantic_type having width=None (falls through to types)
    class DummySymbolWithNoWidthSemanticType:
        width = None
        semantic_type = DummyTypeNoWidth()

    model.symbols["sig2"] = DummySymbolWithNoWidthSemanticType()
    model.types["sig2"] = {"width": 32}

    assert validator._lookup_width("sig2", model) == 32
