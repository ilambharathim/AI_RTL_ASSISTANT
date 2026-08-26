"""
Production Architecture Verification Suite.
Validates AI Gateway, Grounding Validator, Response Validator, Simulator Runner, Closed-Loop Repair Engine, and RESTful Project Routes.
"""

import pytest
from app.ai.evidence_store import EvidenceStore
from app.ai.ai_provider import AIProvider
from app.ai.response_validator import ResponseValidator
from app.ai.grounding_validator import GroundingValidator
from app.simulation.simulator_runner import SimulatorRunner
from app.repair.closed_loop_repair import ClosedLoopRepairEngine
from app.diagnostics.diagnostic import Diagnostic
from app.shared.source_location import SourceLocation
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_ai_provider_gateway_execution():
    store = EvidenceStore(project_name="Gateway_Project")
    loc = SourceLocation(source_file="top.sv", line=10, column=4)
    diag = Diagnostic(code="RIVA2003", category="width", severity="warning", message="Truncation", location=loc)
    store.add_diagnostics([diag])
    
    provider = AIProvider()
    result = provider.process_evidence(store.get_payload())
    
    assert "summary" in result
    assert "findings" in result
    assert len(result["findings"]) == 1


def test_response_validator_valid_and_invalid_schema():
    validator = ResponseValidator()
    
    valid_json = '{"summary": "Clean", "findings": []}'
    is_valid, data, msg = validator.validate_schema(valid_json)
    assert is_valid is True
    assert data["summary"] == "Clean"
    
    invalid_json = '{"bad_key": true}'
    is_valid, data, msg = validator.validate_schema(invalid_json)
    assert is_valid is False


def test_grounding_validator_detects_hallucinations():
    store = EvidenceStore(project_name="Grounding_Test")
    loc = SourceLocation(source_file="top.sv", line=1, column=1)
    diag = Diagnostic(code="RIVA2003", category="width", severity="warning", message="Truncation", location=loc)
    store.add_diagnostics([diag])
    
    validator = GroundingValidator()
    
    # Valid explanation
    valid_exp = {"findings": [{"code": "RIVA2003", "signal": ""}]}
    res = validator.validate_grounding(valid_exp, store.get_payload())
    assert res.is_grounded is True
    
    # Hallucinated explanation
    hallucinated_exp = {"findings": [{"code": "RIVA9999", "signal": "invented_sig"}]}
    res_h = validator.validate_grounding(hallucinated_exp, store.get_payload())
    assert res_h.is_grounded is False
    assert "RIVA9999" in res_h.hallucinated_codes


def test_simulator_runner_execution_and_vcd_capture():
    runner = SimulatorRunner()
    simulators = runner.detect_simulators()
    assert isinstance(simulators, dict)
    
    res = runner.execute_simulation(
        rtl_code="module top; endmodule",
        testbench_code="module tb; endmodule"
    )
    assert res["status"] == "PASSED"
    assert res["vcd_captured"] is True


def test_closed_loop_repair_engine_verification():
    engine = ClosedLoopRepairEngine()
    
    rtl_buggy = "module top(input logic [15:0] in, output logic [7:0] data_out); assign data_out = in; endmodule"
    loc = SourceLocation(source_file="top.sv", line=1, column=1)
    diag = Diagnostic(code="RIVA2003", category="width", severity="warning", message="Width mismatch", location=loc)
    
    repair_res = engine.attempt_repair(rtl_buggy, diag)
    assert "[15:0] data_out" in repair_res.patched_code


def test_restful_projects_api_lifecycle():
    # 1. Create project
    create_res = client.post("/api/projects", json={"name": "Lifecycle Project", "description": "Test"})
    assert create_res.status_code == 200
    proj_id = create_res.json()["project_id"]
    
    # 2. Upload file
    upload_res = client.post(f"/api/projects/{proj_id}/files", json={"filename": "design.sv", "category": "rtl", "content": "module top; endmodule"})
    assert upload_res.status_code == 200
    
    # 3. Get status
    status_res = client.get(f"/api/projects/{proj_id}/status")
    assert status_res.status_code == 200
    assert status_res.json()["files_count"] == 1
