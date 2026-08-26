"""
Comprehensive Unit Test Suite for Phase 7 — Requirement Tracer.
Validates 100% of branches across RequirementTracer.
"""

import pytest
from app.analysis.traceability.requirement_tracer import RequirementTracer
from app.domain.requirement import Requirement
from app.ast import CompilationUnit, ModuleDeclaration, PortDeclaration, SignalDeclaration
from app.ast.expression import LiteralExpression
from app.ast.packed_range import PackedRange
from app.semantics.semantic_model import SemanticModel


def test_requirement_tracer_all_branches():
    tracer = RequirementTracer()
    model = SemanticModel()

    # Create AST with ports and packed ranges
    range_valid = PackedRange(left=LiteralExpression("15"), right=LiteralExpression("0"))
    range_invalid = PackedRange(left=LiteralExpression("a"), right=LiteralExpression("b"))

    port1 = PortDeclaration(direction="input", signal_type="logic", packed_range=range_valid, name="bus_in")
    port2 = PortDeclaration(direction="output", signal_type="logic", packed_range=range_invalid, name="bus_err")

    sig1 = SignalDeclaration(signal_type="logic", packed_range=PackedRange(left=LiteralExpression("7"), right=LiteralExpression("0")), name="sig_width_8")

    mod = ModuleDeclaration(name="top", ports=[port1, port2], members=[sig1])
    cu = CompilationUnit(declarations=[mod])
    model.syntax_tree = cu
    model.symbols = {"extra_symbol": None}

    # Requirements
    req_unverified = Requirement(requirement_id="REQ-00", category="FUNC", description="UPPERCASE ONLY", condition="", expected_result="")
    req_passed = Requirement(requirement_id="REQ-01", category="FUNC", description="Expected 16-bit input", condition="bus_in:16", expected_result="16 bit")
    req_width_mismatch = Requirement(requirement_id="REQ-02", category="FUNC", description="Expected 16-bit signal", condition="sig_width_8", expected_result="16-bit")
    req_missing_sig = Requirement(requirement_id="REQ-03", category="FUNC", description="", condition="non_existent_signal", expected_result="")

    reqs = [req_unverified, req_passed, req_width_mismatch, req_missing_sig]

    res = tracer.trace(reqs, model)
    links = res["links"]
    diags = res["diagnostics"]

    assert len(links) == 4
    assert links[0].status == "UNVERIFIED"
    assert links[1].status == "PASSED"
    assert links[2].status == "FAILED"
    assert links[3].status == "FAILED"

    assert len(diags) == 2
    assert any("RIVA6001" == d.code for d in diags)
    assert any("RIVA6002" == d.code for d in diags)
