"""
Focused Unit Tests for Phase 9 — Typed IR Optimization Passes.
Tests edge cases in TypedConstantFolding and TypedConstantPropagation:
- Division by zero
- Non-numeric literal parsing exception handling
- Unary operators (!, ~, +)
- Binary operator fold when only 1 side changes
- Propagation when identifier is not in constants or expression is unknown
"""

import pytest
from app.ir.ir_expression import IRLiteral, IRIdentifier, IRBinary, IRUnary
from app.optimization.typed_ir.typed_constant_folding import TypedConstantFolding
from app.optimization.typed_ir.typed_constant_propagation import TypedConstantPropagation
from app.semantics.semantic_model import SemanticModel


def test_typed_constant_folding_edge_cases():
    folder = TypedConstantFolding()

    # 1. None elaboration
    model = SemanticModel()
    model.elaboration = None
    res = folder.run(model, context=None)
    assert res.changed is False

    # 2. None expression
    node, changed = folder._fold(None)
    assert node is None and changed is False

    # 3. Division by zero
    div_zero = IRBinary("/", IRLiteral("10"), IRLiteral("0"))
    node, changed = folder._fold(div_zero)
    assert changed is False

    # 4. Invalid integer literal string in binary
    bad_lit = IRBinary("+", IRLiteral("abc"), IRLiteral("10"))
    node, changed = folder._fold(bad_lit)
    assert changed is False

    # 5. Invalid integer literal string in unary
    bad_un = IRUnary("-", IRLiteral("xyz"))
    node, changed = folder._fold(bad_un)
    assert changed is False

    # 6. Unary operators !, ~, +
    un_not = IRUnary("!", IRLiteral("0"))
    node_not, c_not = folder._fold(un_not)
    assert c_not is True and node_not.value == "1"

    un_inv = IRUnary("~", IRLiteral("0"))
    node_inv, c_inv = folder._fold(un_inv)
    assert c_inv is True and node_inv.value == "-1"

    un_pos = IRUnary("+", IRLiteral("42"))
    node_pos, c_pos = folder._fold(un_pos)
    assert c_pos is True and node_pos.value == "42"

    # 7. Unary operand changed but not fold to literal (e.g. nested unaries)
    un_nested = IRUnary("-", IRBinary("+", IRIdentifier("a"), IRLiteral("2")))
    node_un_nested, c_un = folder._fold(un_nested)
    assert c_un is False


def test_typed_constant_propagation_edge_cases():
    prop = TypedConstantPropagation()

    # 1. None elaboration
    model = SemanticModel()
    model.elaboration = None
    res = prop.run(model, context=None)
    assert res.changed is False

    # 2. None expression
    node, changed = prop._propagate(None, {})
    assert node is None and changed is False

    # 3. Identifier not in constants
    ident = IRIdentifier("unknown_var")
    node, changed = prop._propagate(ident, {"other_var": 5})
    assert node is ident and changed is False

    # 4. Literal / unknown node type in propagation
    lit = IRLiteral("100")
    node, changed = prop._propagate(lit, {"x": 10})
    assert node is lit and changed is False

    # 5. Unary expression propagation where operand changes
    un_prop = IRUnary("-", IRIdentifier("x"))
    node_un, c_un = prop._propagate(un_prop, {"x": 15})
    assert c_un is True
    assert isinstance(node_un, IRUnary)
    assert node_un.operand.value == "15"

    # 6. Binary expression propagation where right child changes
    bin_prop = IRBinary("+", IRLiteral("5"), IRIdentifier("y"))
    node_bin, c_bin = prop._propagate(bin_prop, {"y": 20})
    assert c_bin is True
    assert isinstance(node_bin, IRBinary)
    assert node_bin.right.value == "20"
