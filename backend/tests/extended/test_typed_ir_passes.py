"""
Comprehensive Unit Test Suite for Typed IR Optimization Passes.
Covers 100% of branches for:
- TypedDeadAssignmentElimination
- TypedControlFlowSimplification
- TypedConstantFolding
- TypedConstantPropagation
"""

import pytest
from app.ir.ir_module import IRModule
from app.ir.ir_statement import IRAssignment, IRIf, IRBlock
from app.ir.ir_expression import IRIdentifier, IRLiteral, IRBinary, IRUnary
from app.optimization.typed_ir.typed_dead_assignment_elimination import TypedDeadAssignmentElimination
from app.optimization.typed_ir.typed_control_flow_simplification import TypedControlFlowSimplification
from app.optimization.typed_ir.typed_constant_folding import TypedConstantFolding
from app.optimization.typed_ir.typed_constant_propagation import TypedConstantPropagation
from app.semantics.semantic_model import SemanticModel


def test_typed_dead_assignment_elimination_all_branches():
    model = SemanticModel()
    pass_obj = TypedDeadAssignmentElimination()

    # Early exit on missing elaboration
    res0 = pass_obj.run(model, {})
    assert res0.changed is False

    # Setup IR Module
    mod = IRModule("top")
    # Dead assignment: dead_var = 10
    assign_dead = IRAssignment(target="dead_var", expression=IRLiteral("10"))
    # Live assignment with Unary expression: a = -x
    assign_a = IRAssignment(target="a", expression=IRUnary("-", IRIdentifier("x")))
    # Read of a: b = a + 5
    assign_b = IRAssignment(target="b", expression=IRBinary("+", IRIdentifier("a"), IRLiteral("5")))
    # Read of b: c = b
    assign_c = IRAssignment(target="c", expression=IRIdentifier("b"))
    # Statement using c in expression without unread target
    stmt_read_c = IRAssignment(target="b", expression=IRIdentifier("c"))

    # Add a non-dict module statement to hit AttributeError/hasattr check
    class NonStmt:
        pass

    mod.statements = [assign_dead, assign_a, assign_b, assign_c, stmt_read_c, NonStmt()]
    model.elaboration = {"ir": {"top": mod, "empty_mod": "not_a_module"}}

    res = pass_obj.run(model, {})
    assert res.changed is True
    targets = [s.target for s in mod.statements if isinstance(s, IRAssignment)]
    assert "dead_var" not in targets
    assert "a" in targets


def test_typed_control_flow_simplification_all_branches():
    model = SemanticModel()
    pass_obj = TypedControlFlowSimplification()

    # Early exit on missing elaboration
    res0 = pass_obj.run(model, {})
    assert res0.changed is False

    mod = IRModule("top")
    # 1. if (1) then_single_stmt (non-IRBlock)
    stmt_single = IRAssignment(target="x", expression=IRLiteral("1"))
    if_true_single = IRIf(condition=IRLiteral("1"), then_branch=stmt_single)

    # 2. if (1) then_block (IRBlock)
    if_true_block = IRIf(condition=IRLiteral("1"), then_branch=IRBlock([stmt_single]))

    # 3. if (0) then_stmt else else_block
    stmt_else = IRAssignment(target="y", expression=IRLiteral("2"))
    if_false_block = IRIf(condition=IRLiteral("0"), then_branch=stmt_single, else_branch=IRBlock([stmt_else]))

    # 4. if (0) then_stmt else else_single
    if_false_single = IRIf(condition=IRLiteral("0"), then_branch=stmt_single, else_branch=stmt_else)

    # 5. if (cond) then_stmt (non-constant condition)
    if_nonconst = IRIf(condition=IRIdentifier("cond"), then_branch=stmt_single)

    mod.statements = [if_true_single, if_true_block, if_false_block, if_false_single, if_nonconst]
    model.elaboration = {"ir": {"top": mod}}

    res = pass_obj.run(model, {})
    assert res.changed is True


def test_typed_constant_folding_all_branches():
    model = SemanticModel()
    pass_obj = TypedConstantFolding()

    # Early exit on missing elaboration
    res0 = pass_obj.run(model, {})
    assert res0.changed is False

    mod = IRModule("top")

    # Binary arithmetic & comparisons & bitwise
    expr_add = IRBinary("+", IRLiteral("2"), IRLiteral("3"))
    expr_sub = IRBinary("-", IRLiteral("8"), IRLiteral("3"))
    expr_mul = IRBinary("*", IRLiteral("2"), IRLiteral("4"))
    expr_div = IRBinary("/", IRLiteral("8"), IRLiteral("2"))
    expr_div0 = IRBinary("/", IRLiteral("8"), IRLiteral("0"))
    expr_and = IRBinary("&", IRLiteral("4"), IRLiteral("3"))
    expr_or = IRBinary("|", IRLiteral("4"), IRLiteral("3"))
    expr_xor = IRBinary("^", IRLiteral("4"), IRLiteral("3"))
    expr_eq = IRBinary("==", IRLiteral("4"), IRLiteral("4"))
    expr_neq = IRBinary("!=", IRLiteral("4"), IRLiteral("4"))
    expr_lt = IRBinary("<", IRLiteral("3"), IRLiteral("5"))
    expr_lte = IRBinary("<=", IRLiteral("5"), IRLiteral("5"))
    expr_gt = IRBinary(">", IRLiteral("5"), IRLiteral("3"))
    expr_gte = IRBinary(">=", IRLiteral("5"), IRLiteral("5"))

    # Unary ops
    expr_neg = IRUnary("-", IRLiteral("5"))
    expr_pos = IRUnary("+", IRLiteral("5"))
    expr_not = IRUnary("!", IRLiteral("0"))
    expr_inv = IRUnary("~", IRLiteral("0"))

    # Non-constant / nested exprs
    expr_nested_bin = IRBinary("+", IRIdentifier("a"), IRBinary("+", IRLiteral("2"), IRLiteral("3")))
    expr_nested_un = IRUnary("-", IRUnary("-", IRLiteral("5")))

    stmts = [
        IRAssignment("r1", expr_add),
        IRAssignment("r2", expr_sub),
        IRAssignment("r3", expr_mul),
        IRAssignment("r4", expr_div),
        IRAssignment("r5", expr_div0),
        IRAssignment("r6", expr_and),
        IRAssignment("r7", expr_or),
        IRAssignment("r8", expr_xor),
        IRAssignment("r9", expr_eq),
        IRAssignment("r10", expr_neq),
        IRAssignment("r11", expr_lt),
        IRAssignment("r12", expr_lte),
        IRAssignment("r13", expr_gt),
        IRAssignment("r14", expr_gte),
        IRAssignment("r15", expr_neg),
        IRAssignment("r16", expr_pos),
        IRAssignment("r17", expr_not),
        IRAssignment("r18", expr_inv),
        IRAssignment("r19", expr_nested_bin),
        IRAssignment("r20", expr_nested_un),
    ]

    mod.statements = stmts
    model.elaboration = {"ir": {"top": mod}}

    res = pass_obj.run(model, {})
    assert res.changed is True

    assert stmts[0].expression.value == "5"
    assert stmts[1].expression.value == "5"
    assert stmts[2].expression.value == "8"
    assert stmts[3].expression.value == "4"
    assert isinstance(stmts[4].expression, IRBinary)
    assert stmts[5].expression.value == "0"
    assert stmts[6].expression.value == "7"
    assert stmts[7].expression.value == "7"
    assert stmts[8].expression.value == "1"
    assert stmts[9].expression.value == "0"
    assert stmts[10].expression.value == "1"
    assert stmts[11].expression.value == "1"
    assert stmts[12].expression.value == "1"
    assert stmts[13].expression.value == "1"
    assert stmts[14].expression.value == "-5"
    assert stmts[15].expression.value == "5"
    assert stmts[16].expression.value == "1"
    assert stmts[17].expression.value == "-1"


def test_typed_constant_propagation_all_branches():
    model = SemanticModel()
    model.constant_values = {"WIDTH": 16, "C1": 10}
    pass_obj = TypedConstantPropagation()

    # Early exit on missing elaboration
    res0 = pass_obj.run(model, {})
    assert res0.changed is False

    mod = IRModule("top")

    expr_id = IRIdentifier("WIDTH")
    expr_bin = IRBinary("+", IRIdentifier("C1"), IRIdentifier("unknown_var"))
    expr_un = IRUnary("-", IRIdentifier("WIDTH"))

    stmts = [
        IRAssignment("out1", expr_id),
        IRAssignment("out2", expr_bin),
        IRAssignment("out3", expr_un),
    ]

    mod.statements = stmts
    model.elaboration = {"ir": {"top": mod}}

    res = pass_obj.run(model, {})
    assert res.changed is True

    assert isinstance(stmts[0].expression, IRLiteral)
    assert stmts[0].expression.value == "16"

    assert isinstance(stmts[1].expression, IRBinary)
    assert isinstance(stmts[1].expression.left, IRLiteral)
    assert stmts[1].expression.left.value == "10"

    assert isinstance(stmts[2].expression, IRUnary)
    assert isinstance(stmts[2].expression.operand, IRLiteral)
    assert stmts[2].expression.operand.value == "16"
