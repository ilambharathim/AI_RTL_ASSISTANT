"""
Comprehensive Unit Test Suite for Phase 3 — Port and Instance Validation.
Validates 100% of branches across PortValidator and InstanceValidator.
"""

import pytest
from app.ast import CompilationUnit, ModuleDeclaration, PortDeclaration
from app.ast.module_instance import ModuleInstance
from app.ast.port_connection import PortConnection
from app.ast.expression import IdentifierExpression
from app.elaboration.validation.port_validator import PortValidator
from app.elaboration.validation.instance_validator import InstanceValidator
from app.semantics.semantic_model import SemanticModel


def test_instance_validator_branches():
    val = InstanceValidator()

    # Module definitions
    sub = ModuleDeclaration(name="sub_mod", ports=[], members=[])
    inst_valid = ModuleInstance(module_name="sub_mod", parameter_overrides=[], instance_name="u_valid", connections=[])
    inst_unknown = ModuleInstance(module_name="non_existent", parameter_overrides=[], instance_name="u_unk", connections=[])

    class NonModule:
        pass

    top = ModuleDeclaration(name="top", ports=[], members=[inst_valid, inst_unknown, NonModule()])
    cu = CompilationUnit(declarations=[sub, top, NonModule()])

    diags = val.validate(cu)
    assert len(diags) == 1
    assert "Unknown module 'non_existent' instantiated as 'u_unk'" in diags[0]


def test_port_validator_all_branches():
    validator = PortValidator()
    model = SemanticModel()

    # Port definitions
    port_a = PortDeclaration(direction="input", signal_type="logic", packed_range=None, name="clk")
    port_b = PortDeclaration(direction="input", signal_type="logic", packed_range=None, name="data_in")
    port_c = PortDeclaration(direction="output", signal_type="logic", packed_range=None, name="data_out")

    sub = ModuleDeclaration(name="sub_mod", ports=[port_a, port_b, port_c], members=[])

    # Connections
    # 1. Duplicate connection to clk
    conn1 = PortConnection("clk", IdentifierExpression("sys_clk"))
    conn2 = PortConnection("clk", IdentifierExpression("sys_clk"))
    # 2. Unknown port
    conn3 = PortConnection("unknown_port", IdentifierExpression("sig_x"))
    # 3. Width mismatch (port data_in expected 8, signal data_sig got 16)
    conn4 = PortConnection("data_in", IdentifierExpression("data_sig"))

    inst = ModuleInstance(module_name="sub_mod", parameter_overrides=[], instance_name="u_sub", connections=[conn1, conn2, conn3, conn4])

    top = ModuleDeclaration(name="top", ports=[], members=[inst])
    cu = CompilationUnit(declarations=[sub, top])

    # Setup widths across semantic_types, symbols, and types dict
    class WidthType:
        def __init__(self, w):
            self.width = w

    model.semantic_types = {
        "clk": WidthType(1),
        "sys_clk": WidthType(1),
        "data_in": WidthType(8),
    }

    class SymbolWithSemType:
        def __init__(self, w):
            self.semantic_type = WidthType(w)

    class SymbolWithWidth:
        def __init__(self, w):
            self.width = w

    model.symbols = {
        "data_sig": SymbolWithSemType(16),
        "symbol_w": SymbolWithWidth(4),
    }

    model.types = {
        "dict_type": {"width": 8},
        "obj_type": WidthType(8),
    }

    diags = validator.validate(cu, model)

    assert len(diags) >= 3
    assert any("Duplicate connection to port 'clk'" in d for d in diags)
    assert any("Unknown port 'unknown_port'" in d for d in diags)
    assert any("Width mismatch on port 'data_in'" in d for d in diags)
    assert any("Missing connection for port 'data_out'" in d for d in diags)

    # Test lookup_width fallbacks directly
    assert validator._lookup_width("clk", model) == 1
    assert validator._lookup_width("data_sig", model) == 16
    assert validator._lookup_width("symbol_w", model) == 4
    assert validator._lookup_width("dict_type", model) == 8
    assert validator._lookup_width("obj_type", model) == 8
    assert validator._lookup_width("non_existent", model) is None
