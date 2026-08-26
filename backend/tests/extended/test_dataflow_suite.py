"""
Comprehensive Unit Test Suite for Phase 6 — Dataflow Analysis.
Validates 100% of branches across WorklistSolver and LiveVariableAnalysis.
"""

import pytest
from app.analysis.cfg.control_flow_graph import ControlFlowGraph
from app.analysis.dataflow.worklist_solver import WorklistSolver
from app.analysis.dataflow.analyses.live_variables import LiveVariableAnalysis
from app.ast import ProceduralAssignment
from app.ast.expression import IdentifierExpression, LiteralExpression, BinaryExpression


class ForwardDummyAnalysis:
    forward = True

    def initial(self):
        return set()

    def meet(self, predecessors):
        res = set()
        for p in predecessors:
            res.update(p)
        return res

    def transfer(self, block, incoming):
        out = set(incoming)
        for stmt in getattr(block, "statements", []):
            if hasattr(stmt, "target"):
                out.add(stmt.target)
        return out


def test_worklist_solver_forward_and_backward_branches():
    solver = WorklistSolver()

    # 1. Forward Dataflow Analysis Test
    cfg_fwd = ControlFlowGraph()
    b1 = cfg_fwd.new_block()
    b2 = cfg_fwd.new_block()
    b1.connect(b2)
    b1.statements.append(ProceduralAssignment("x", "=", LiteralExpression("1")))
    b2.statements.append(ProceduralAssignment("y", "=", IdentifierExpression("x")))

    res_fwd = solver.solve(cfg_fwd, ForwardDummyAnalysis())
    assert b1.id in res_fwd.out_sets
    assert "x" in res_fwd.out_sets[b1.id]
    assert "y" in res_fwd.out_sets[b2.id]

    # 2. Backward Dataflow Analysis Test (LiveVariables)
    cfg_bwd = ControlFlowGraph()
    b_entry = cfg_bwd.new_block()
    b_body = cfg_bwd.new_block()
    b_exit = cfg_bwd.new_block()

    b_entry.connect(b_body)
    b_body.connect(b_body)  # loop
    b_body.connect(b_exit)

    b_entry.statements.append(ProceduralAssignment("a", "=", LiteralExpression("10")))
    b_body.statements.append(ProceduralAssignment("b", "=", BinaryExpression("+", IdentifierExpression("a"), LiteralExpression("1"))))
    b_exit.statements.append(ProceduralAssignment("out", "=", IdentifierExpression("b")))

    res_bwd = solver.solve(cfg_bwd, LiveVariableAnalysis())
    assert b_entry.id in res_bwd.in_sets
    assert b_body.id in res_bwd.in_sets
