"""
Full end-to-end integration test for EvidenceStore, AIReasoningEngine, and ConsolidatedReportGenerator.
"""

from app.parsers.rtl.lexer import RTLLexer
from app.parsers.rtl.parser import RTLParser
from app.semantics.semantic_analyzer import SemanticAnalyzer
from app.elaboration.elaborator import Elaborator
from app.elaboration.hierarchy_builder import HierarchyTreeBuilder
from app.domain.requirement import Requirement
from app.analysis.traceability.requirement_tracer import RequirementTracer
from app.diagnostics.diagnostic_engine import DiagnosticEngine
from app.ai.evidence_store import EvidenceStore
from app.ai.ai_reasoning_engine import AIReasoningEngine
from app.reporting.report_generator import ConsolidatedReportGenerator


def test_full_pipeline_to_report():
    code = """
    module counter(
        input logic clk,
        input logic reset,
        output logic [7:0] count
    );
        always_comb begin
            count = count + 1;
        end
    endmodule
    """

    lexer = RTLLexer()
    tokens = lexer.tokenize(code)

    parser = RTLParser()
    parse_result = parser.parse(tokens.tokens)
    assert parse_result.successful
    syntax_tree = parse_result.syntax_tree

    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(syntax_tree)

    elaborator = Elaborator()
    elaborated_model = elaborator.elaborate(syntax_tree, semantic_model)

    hierarchy_builder = HierarchyTreeBuilder()
    trees = hierarchy_builder.build_tree(syntax_tree)

    diagnostic_engine = DiagnosticEngine()
    diagnostics = diagnostic_engine.analyze(semantic_model)

    req = Requirement(
        requirement_id="REQ-CNT-01",
        category="FUNCTIONAL",
        description="The count signal shall be an 8-bit output register.",
        condition="count",
        expected_result="8-bit output",
    )

    tracer = RequirementTracer()
    trace_result = tracer.trace([req], semantic_model)

    evidence_store = EvidenceStore(project_name="Counter_Module_Test")
    evidence_store.add_diagnostics(diagnostics)
    evidence_store.add_traceability_links(trace_result["links"])
    evidence_store.add_diagnostics(trace_result["diagnostics"])
    evidence_store.set_hierarchy_summary({"top_module": trees[0].module_name, "children": len(trees[0].children)})

    payload = evidence_store.get_payload()

    ai_engine = AIReasoningEngine()
    explanation = ai_engine.generate_explanation(payload)
    prompt = ai_engine.format_llm_prompt(payload)

    assert explanation is not None
    assert "summary" in explanation
    assert "Counter_Module_Test" in prompt

    report_gen = ConsolidatedReportGenerator(ai_engine)
    md_report = report_gen.generate_markdown_report(payload)
    json_report = report_gen.generate_json_report(payload)

    assert "# RIVA Consolidated Verification Report" in md_report
    assert "Counter_Module_Test" in json_report
    assert "REQ-CNT-01" in md_report
