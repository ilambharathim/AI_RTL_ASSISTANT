"""
RIVA Golden End-to-End Pipeline Integration Test.
Validates the complete 15-stage verification lifecycle across Specification, SystemVerilog RTL, AST, Semantics, Elaboration, CFG, Diagnostics, Waveforms, AI Gateway, and Reports.
"""

import pytest
from app.parsers.rtl.lexer import RTLLexer
from app.parsers.rtl.parser import RTLParser
from app.semantics.semantic_analyzer import SemanticAnalyzer
from app.elaboration.hierarchy_builder import HierarchyTreeBuilder
from app.analysis.cfg.cfg_builder import CFGBuilder
from app.diagnostics.diagnostic_engine import DiagnosticEngine
from app.analysis.traceability.requirement_tracer import RequirementTracer
from app.parsers.specification.normalizer import DocumentNormalizer
from app.parsers.specification.lexer import SpecificationLexer
from app.parsers.specification.parser import SpecificationParser
from app.parsers.specification.semantic_builder import SpecificationSemanticBuilder
from app.ai.evidence_store import EvidenceStore
from app.ai.ai_provider import AIProvider
from app.reporting.report_generator import ConsolidatedReportGenerator
from app.repair.closed_loop_repair import ClosedLoopRepairEngine
from app.diagnostics.diagnostic import Diagnostic
from app.shared.source_location import SourceLocation
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_golden_riva_pipeline_clean_design():
    rtl_code = """
    module top_clean(
        input logic [15:0] in_data,
        output logic [15:0] out_data
    );
        assign out_data = in_data;
    endmodule
    """

    spec_code = """
    [REQ-001]
    Category: FUNCTIONAL
    Signal: out_data
    Description: Expected 16-bit output.
    Expected: 16 bits
    """

    # 1. Lexer & Parser
    tokens = RTLLexer().tokenize(rtl_code)
    parse_res = RTLParser().parse(tokens.tokens)
    assert parse_res.syntax_tree is not None

    # 2. Semantic Analysis
    model = SemanticAnalyzer().analyze(parse_res.syntax_tree)
    assert model is not None

    # 3. Hierarchy Elaboration
    hierarchy = HierarchyTreeBuilder().build_tree(parse_res.syntax_tree)
    assert len(hierarchy) >= 1

    # 4. CFG & Dataflow
    cfg = CFGBuilder().build(parse_res.syntax_tree)
    assert cfg is not None

    # 5. Diagnostics
    diags = DiagnosticEngine().analyze(model)
    assert len(diags) == 0

    # 6. Requirement Tracer
    normalized_spec = DocumentNormalizer.normalize(spec_code)
    spec_tokens = SpecificationLexer(normalized_spec, source_file="spec.txt").tokenize()
    spec_doc = SpecificationParser(spec_tokens).parse()
    spec_ir = SpecificationSemanticBuilder(spec_doc).build().specification

    tracer = RequirementTracer()
    trace_res = tracer.trace(spec_ir.requirements, model)
    links = trace_res.get("links", [])
    assert isinstance(links, list)

    # 7. Evidence Store & AI Gateway
    store = EvidenceStore(project_name="Golden_Clean")
    store.add_diagnostics(diags)
    store.add_traceability_links(links)

    provider = AIProvider()
    ai_result = provider.process_evidence(store.get_payload())
    assert ai_result["confidence_score"] >= 80

    # 8. Report Generator
    report_gen = ConsolidatedReportGenerator()
    report = report_gen.generate_markdown_report(store.get_payload())
    assert "Golden_Clean" in report


def test_golden_riva_pipeline_buggy_design_and_closed_loop_repair():
    rtl_buggy = "module top(input logic [15:0] in, output logic [7:0] data_out); assign data_out = in; endmodule"

    loc = SourceLocation(source_file="top.sv", line=1, column=1)
    diag = Diagnostic(code="RIVA2003", category="width", severity="warning", message="Width mismatch", location=loc)

    # Closed-Loop Repair
    repair_engine = ClosedLoopRepairEngine()
    repair_res = repair_engine.attempt_repair(rtl_buggy, diag)
    assert repair_res.is_verified is True
    assert repair_res.diagnostic_removed is True
    assert "[15:0] data_out" in repair_res.patched_code
