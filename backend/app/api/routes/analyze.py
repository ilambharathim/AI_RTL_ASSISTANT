"""
RIVA End-to-End Verification Pipeline API route.
"""

from typing import Optional, List, Dict, Any
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, status
from pydantic import BaseModel
import re

from app.parsers.rtl.lexer import RTLLexer
from app.parsers.rtl.parser import RTLParser
from app.semantics.semantic_analyzer import SemanticAnalyzer
from app.elaboration.elaborator import Elaborator
from app.elaboration.hierarchy_builder import HierarchyTreeBuilder
from app.domain.requirement import Requirement
from app.analysis.traceability.requirement_tracer import RequirementTracer
from app.diagnostics.diagnostic_engine import DiagnosticEngine
from app.simulation.waveform_analyzer import WaveformAnalyzer
from app.simulation.simulator_runner import SimulatorRunner
from app.analysis.design_metadata_extractor import DesignMetadataExtractor
from app.ai.evidence_store import EvidenceStore
from app.ai.ai_reasoning_engine import AIReasoningEngine
from app.reporting.report_generator import ConsolidatedReportGenerator

router = APIRouter()


class AnalyzeRequest(BaseModel):
    rtl_code: str
    spec_code: str
    testbench_code: Optional[str] = ""
    vcd_content: Optional[str] = ""


def parse_requirements_from_text(spec_text: str) -> List[Requirement]:
    """Extract requirements from specification text ([REQ-xxx] format)."""
    spec_text = (spec_text or "").strip()
    if not spec_text:
        return []

    requirements = []
    blocks = re.split(r'\[(REQ-[A-Za-z0-9_\-]+)\]', spec_text)

    if len(blocks) <= 1:
        return []

    for i in range(1, len(blocks), 2):
        req_id = blocks[i]
        body = blocks[i + 1] if i + 1 < len(blocks) else ""

        desc_match = re.search(r'^\s*Description\s*:\s*(.+)$', body, re.IGNORECASE | re.MULTILINE)
        if desc_match:
            desc = desc_match.group(1).strip()
        else:
            lines = [l.strip() for l in body.splitlines() if l.strip() and not re.match(r'^(Signal|Condition|Target|Expected|Category)\s*:', l, re.IGNORECASE)]
            desc = lines[0] if lines else f"Requirement {req_id}"

        sig_match = re.search(r'^\s*(?:Signal|Condition|Target)\s*:\s*([A-Za-z0-9_]+)', body, re.IGNORECASE | re.MULTILINE)
        sig = sig_match.group(1).strip() if sig_match else None

        exp_match = re.search(r'^\s*(?:Expected|Expected Result)\s*:\s*(.+)$', body, re.IGNORECASE | re.MULTILINE)
        exp = exp_match.group(1).strip() if exp_match else "specified behavior"

        cat_match = re.search(r'^\s*Category\s*:\s*([A-Za-z0-9_\-]+)', body, re.IGNORECASE | re.MULTILINE)
        cat = cat_match.group(1).strip() if cat_match else "FUNCTIONAL"

        requirements.append(Requirement(
            requirement_id=req_id,
            category=cat,
            description=desc,
            condition=sig,
            expected_result=exp
        ))

    return requirements



@router.post("/analyze")
def analyze_project(payload: AnalyzeRequest):
    """
    Run full deterministic verification pipeline on submitted RTL, Spec, and Testbench.
    """
    rtl_code = payload.rtl_code.strip()
    spec_code = payload.spec_code.strip()
    
    if not rtl_code:
        raise HTTPException(status_code=400, detail="RTL code cannot be empty.")

    # 1. Lexing
    lexer = RTLLexer()
    lex_res = lexer.tokenize(rtl_code)
    
    # 2. Parsing
    parser = RTLParser()
    parse_res = parser.parse(lex_res.tokens)
    syntax_tree = parse_res.syntax_tree

    # 3. Semantic Analysis
    analyzer = SemanticAnalyzer()
    semantic_model = analyzer.analyze(syntax_tree)

    # 4. Hierarchy Elaboration
    elaborator = Elaborator()
    elaborated_model = elaborator.elaborate(syntax_tree, semantic_model)
    
    hierarchy_builder = HierarchyTreeBuilder()
    hierarchy_trees = hierarchy_builder.build_tree(syntax_tree)

    # 5. Diagnostic Engine
    diagnostic_engine = DiagnosticEngine()
    diagnostics = diagnostic_engine.analyze(semantic_model)

    # 6. Requirement Traceability
    requirements = parse_requirements_from_text(spec_code)
    tracer = RequirementTracer()
    trace_res = tracer.trace(requirements, semantic_model)

    # 7. Waveform Analysis (VCD upload or automated simulation generation)
    waveform_analysis = {}
    wf_observations = []
    if payload.vcd_content:
        wf_analyzer = WaveformAnalyzer()
        waveform_res = wf_analyzer.analyze_vcd_text(payload.vcd_content, source="uploaded")
        waveform_analysis = waveform_res
        wf_observations = waveform_res.get("observations_raw", [])
    elif payload.testbench_code and payload.testbench_code.strip():
        runner = SimulatorRunner()
        waveform_res = runner.execute_simulation(rtl_code, payload.testbench_code.strip())
        waveform_analysis = waveform_res
        wf_observations = waveform_res.get("observations_raw", [])

    # 8. Evidence Store & Grounded AI
    evidence_store = EvidenceStore(project_name="RIVA_User_Project")
    evidence_store.add_diagnostics(diagnostics)
    evidence_store.add_diagnostics(trace_res["diagnostics"])
    evidence_store.add_traceability_links(trace_res["links"])
    if wf_observations:
        evidence_store.add_waveform_observations(wf_observations)

    
    top_name = hierarchy_trees[0].module_name if hierarchy_trees else "top"
    child_count = len(hierarchy_trees[0].children) if hierarchy_trees else 0
    evidence_store.set_hierarchy_summary({"top_module": top_name, "children": child_count})

    evidence_payload = evidence_store.get_payload()

    ai_engine = AIReasoningEngine()
    explanation = ai_engine.generate_explanation(evidence_payload)

    # 9. Consolidated Report
    report_gen = ConsolidatedReportGenerator(ai_engine)
    md_report = report_gen.generate_markdown_report(evidence_payload)
    json_report = report_gen.generate_json_report(evidence_payload)

    # Format diagnostics for response
    diag_list = []
    all_diags = diagnostics + trace_res["diagnostics"]
    for d in all_diags:
        diag_list.append({
            "code": getattr(d, "code", "RIVA1000"),
            "category": getattr(d, "category", "Verification Diagnostic"),
            "severity": str(getattr(d, "severity", "warning")).lower().replace("diagnosticseverity.", ""),
            "message": getattr(d, "message", "Diagnostic triggered"),
            "suggestion": getattr(d, "suggestion", "Review SystemVerilog signal width and logic assignment"),
            "location": f"line {d.location.line}:{d.location.column}" if hasattr(d, "location") and d.location else "RTL Source"
        })

    # Format hierarchy for response
    hierarchy_data = []
    for tree in hierarchy_trees:
        children_list = []
        for child in tree.children:
            children_list.append({
                "instance_name": getattr(child, "instance_name", getattr(child, "name", "")),
                "module_name": child.module_name,
                "parameters": getattr(child, "parameters", {})
            })
        hierarchy_data.append({
            "module_name": tree.module_name,
            "children": children_list
        })

    # Format traceability links
    links_list = []
    for link in trace_res["links"]:
        links_list.append({
            "requirement_id": link.requirement_id,
            "signal_name": link.target_signal,
            "status": link.status,
            "expected": getattr(link, "details", "Verified Requirement"),
            "actual": getattr(link, "details", "Completed")
        })

    # Format design metadata
    meta_extractor = DesignMetadataExtractor()
    design_metadata = meta_extractor.extract_metadata(syntax_tree, semantic_model)

    return {
        "status": "success",
        "top_module": top_name,
        "design_metadata": design_metadata,
        "diagnostics": diag_list,
        "hierarchy": hierarchy_data,
        "traceability": links_list,
        "waveform": waveform_analysis,
        "explanation": explanation,
        "reports": {
            "markdown": md_report,
            "json": json_report
        }
    }
