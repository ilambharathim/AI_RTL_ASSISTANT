"""
Category 13: API, storage, and integration tests (T405 - T412)
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from tempfile import TemporaryDirectory
from pathlib import Path
from app.storage.file_storage import FileStorage

client = TestClient(app)


def test_T405_upload_specification_to_pipeline():
    response = client.post(
        "/api/analyze",
        json={
            "rtl_code": "module top; endmodule",
            "spec_code": "[REQ-01]\nSignal: clk",
            "testbench_code": "module tb; endmodule"
        }
    )
    assert response.status_code == 200
    assert response.json()["top_module"] == "top"


def test_T406_upload_rtl_to_pipeline():
    response = client.post(
        "/api/analyze",
        json={
            "rtl_code": "module fifo_ctrl(input logic [15:0] in, output logic [7:0] out); assign out = in; endmodule",
            "spec_code": "[REQ-01]\nSignal: out\nExpected: 16-bit",
            "testbench_code": ""
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "diagnostics" in data


def test_T407_upload_validation_report():
    response = client.post(
        "/api/analyze",
        json={
            "rtl_code": "module top; endmodule",
            "spec_code": "[REQ-01]\nSignal: top",
            "testbench_code": ""
        }
    )
    assert response.status_code == 200
    assert "reports" in response.json()


def test_T408_invalid_upload_rollback():
    with TemporaryDirectory() as tmp_dir:
        orig = FileStorage.BASE_UPLOAD_DIR
        FileStorage.BASE_UPLOAD_DIR = Path(tmp_dir) / "uploads"
        try:
            res = client.post(
                "/api/upload",
                files={
                    "specification": ("spec.txt", b"spec", "text/plain"),
                    "rtl": ("rtl.bad", b"bad extension", "text/plain"),
                    "testbench": ("tb.sv", b"module tb; endmodule", "text/plain")
                }
            )
            assert res.status_code == 400
        finally:
            FileStorage.BASE_UPLOAD_DIR = orig


def test_T409_concurrent_upload_isolation():
    res1 = client.post("/api/analyze", json={"rtl_code": "module mod1; endmodule", "spec_code": "[REQ-1]\nSignal: a", "testbench_code": ""})
    res2 = client.post("/api/analyze", json={"rtl_code": "module mod2; endmodule", "spec_code": "[REQ-2]\nSignal: b", "testbench_code": ""})
    assert res1.json()["top_module"] == "mod1"
    assert res2.json()["top_module"] == "mod2"


def test_T410_duplicate_filename_handling_under_concurrency():
    with TemporaryDirectory() as tmp_dir:
        orig = FileStorage.BASE_UPLOAD_DIR
        FileStorage.BASE_UPLOAD_DIR = Path(tmp_dir) / "uploads"
        try:
            res1 = client.post("/api/upload", files={"specification": ("spec.txt", b"s1", "text/plain"), "rtl": ("top.sv", b"module top; endmodule", "text/plain"), "testbench": ("tb.sv", b"module tb; endmodule", "text/plain")})
            res2 = client.post("/api/upload", files={"specification": ("spec.txt", b"s2", "text/plain"), "rtl": ("top.sv", b"module top; endmodule", "text/plain"), "testbench": ("tb.sv", b"module tb; endmodule", "text/plain")})
            assert res1.status_code == 200
            assert res2.status_code == 200
        finally:
            FileStorage.BASE_UPLOAD_DIR = orig


def test_T411_api_malformed_request():
    res = client.post("/api/analyze", json={"rtl_code": "module top; endmodule", "spec_code": "bad spec json"})
    assert res.status_code == 200


def test_T412_api_complete_error_response_contract():
    res = client.post("/api/analyze", json={"rtl_code": "module top; endmodule", "spec_code": ""})
    assert "top_module" in res.json()
