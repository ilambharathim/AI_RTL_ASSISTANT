from __future__ import annotations

import ast
import importlib
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PASS = 0
FAIL = 0
WARN = 0


def ok(label, detail=""):
    global PASS
    PASS += 1
    print(f"PASS  {label}" + (f" :: {detail}" if detail else ""))


def fail(label, detail=""):
    global FAIL
    FAIL += 1
    print(f"FAIL  {label}" + (f" :: {detail}" if detail else ""))


def warn(label, detail=""):
    global WARN
    WARN += 1
    print(f"WARN  {label}" + (f" :: {detail}" if detail else ""))


def section(title):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


print("=" * 78)
print("RIVA BACKEND FINAL COMPLETION AUDIT")
print("BACKEND ONLY — FRONTEND EXCLUDED")
print("=" * 78)

# ---------------------------------------------------------------------------
# 1. LOCATION / FRONTEND ISOLATION
# ---------------------------------------------------------------------------
section("1. BACKEND SCOPE")

if ROOT.name == "backend":
    ok("Backend working directory", str(ROOT))
else:
    fail("Backend working directory", str(ROOT))

frontend = ROOT.parent / "frontend"
if frontend.exists():
    ok("Frontend exists but is excluded", str(frontend))
else:
    ok("No frontend directory involved")

# ---------------------------------------------------------------------------
# 2. PYTHON
# ---------------------------------------------------------------------------
section("2. PYTHON ENVIRONMENT")

print("Python:", sys.version.split()[0])
print("Executable:", sys.executable)

if sys.version_info >= (3, 10):
    ok("Supported Python version")
else:
    fail("Python version too old")

# ---------------------------------------------------------------------------
# 3. COMPILE
# ---------------------------------------------------------------------------
section("3. PYTHON COMPILE CHECK")

result = subprocess.run(
    [sys.executable, "-m", "compileall", "-q", "app"],
    cwd=ROOT,
)

if result.returncode == 0:
    ok("Python compilation")
else:
    fail("Python compilation")

# ---------------------------------------------------------------------------
# 4. CORE IMPORTS
# ---------------------------------------------------------------------------
section("4. CORE MODULE IMPORT AUDIT")

modules = [
    ("Parser", "app.parsers"),
    ("AST", "app.ast"),
    ("Semantic Analyzer", "app.semantics.semantic_analyzer"),
    ("Type Resolver", "app.semantics.type_checking.type_resolver"),
    ("Width Inference", "app.semantics.passes.width_inference"),
    ("Signedness", "app.semantics.passes.signedness_resolver"),
    ("Expression Checker", "app.semantics.passes.expression_type_checker"),
    ("Assignment Compatibility", "app.semantics.passes.assignment_compatibility_checker"),
    ("Elaboration", "app.elaboration"),
    ("IR", "app.ir"),
    ("Diagnostics", "app.diagnostics"),
    ("CFG", "app.analysis.cfg"),
    ("Dataflow", "app.analysis.dataflow"),
    ("Traceability", "app.analysis.traceability"),
    ("Repair", "app.repair"),
    ("Simulation", "app.simulation"),
    ("Optimization", "app.optimization"),
    ("Reporting", "app.reporting"),
    ("AI", "app.ai"),
    ("Storage", "app.storage"),
    ("API", "app.api"),
    ("Main", "app.main"),
]

for name, module in modules:
    try:
        importlib.import_module(module)
        ok(name, module)
    except Exception as exc:
        fail(name, f"{module}: {type(exc).__name__}: {exc}")

# ---------------------------------------------------------------------------
# 5. FASTAPI
# ---------------------------------------------------------------------------
section("5. FASTAPI APPLICATION")

try:
    from app.main import app

    print("Title :", app.title)
    print("Version:", app.version)
    ok("FastAPI application import")
except Exception as exc:
    fail("FastAPI application import", repr(exc))
    app = None

# ---------------------------------------------------------------------------
# 6. ROUTES
# ---------------------------------------------------------------------------
section("6. ACTUAL REGISTERED API ROUTES")

actual_routes = set()

if app:
    for route in app.routes:
        path = getattr(route, "path", None)
        methods = getattr(route, "methods", None)

        if path and methods:
            for method in methods:
                if method not in {"HEAD", "OPTIONS"}:
                    actual_routes.add((method, path))
                    print(f"{method:8} {path}")

required_routes = {
    ("POST", "/upload"),
    ("POST", "/api/upload"),
    ("POST", "/api/analyze"),
    ("POST", "/api/projects"),
    ("POST", "/api/projects/{project_id}/files"),
    ("GET", "/api/projects/{project_id}/status"),
}

missing = required_routes - actual_routes

if not missing:
    ok("Required API routes registered")
else:
    fail("Required API routes missing", str(sorted(missing)))

# ---------------------------------------------------------------------------
# 7. OPENAPI
# ---------------------------------------------------------------------------
section("7. OPENAPI")

if app:
    try:
        schema = app.openapi()
        paths = schema.get("paths", {})

        for path, methods in sorted(paths.items()):
            print(f"{path:45} {','.join(sorted(methods))}")

        openapi_required = {
            "/upload",
            "/api/upload",
            "/api/analyze",
            "/api/projects",
            "/api/projects/{project_id}/files",
            "/api/projects/{project_id}/status",
        }

        missing_openapi = openapi_required - set(paths)

        if not missing_openapi:
            ok("OpenAPI exposes required routes")
        else:
            fail("OpenAPI routes missing", str(sorted(missing_openapi)))

    except Exception as exc:
        fail("OpenAPI generation", repr(exc))

# ---------------------------------------------------------------------------
# 8. WAVEFORM API CONTRACT
# ---------------------------------------------------------------------------
section("8. SIMULATION / WAVEFORM CONTRACT")

try:
    from app.simulation.waveform_analyzer import WaveformAnalyzer

    analyzer = WaveformAnalyzer()

    methods = [
        name
        for name in dir(analyzer)
        if not name.startswith("_") and callable(getattr(analyzer, name))
    ]

    print("WaveformAnalyzer methods:")
    for method in methods:
        print(" ", method)

    if hasattr(analyzer, "analyze_vcd_text"):
        ok("WaveformAnalyzer.analyze_vcd_text exists")
    else:
        fail(
            "WaveformAnalyzer.analyze_vcd_text",
            "API route currently calls this method but it does not exist",
        )

except Exception as exc:
    fail("WaveformAnalyzer import", repr(exc))

# ---------------------------------------------------------------------------
# 9. ANALYZE ROUTE STATIC CONTRACT
# ---------------------------------------------------------------------------
section("9. ANALYZE ROUTE CONTRACT")

analyze_file = ROOT / "app/api/routes/analyze.py"

if analyze_file.exists():
    text = analyze_file.read_text(errors="replace")

    checks = {
        "RTL input": "rtl_code" in text,
        "Specification input": "spec_code" in text,
        "Testbench input": "testbench_code" in text,
        "VCD input": "vcd_content" in text,
        "Semantic analysis": "SemanticAnalyzer" in text,
        "Elaboration": "Elaborator" in text,
        "Traceability": "RequirementTracer" in text,
        "Waveform analysis": "WaveformAnalyzer" in text,
        "Evidence store": "EvidenceStore" in text,
        "AI reasoning": "AIReasoningEngine" in text,
        "Reporting": "ConsolidatedReportGenerator" in text,
    }

    for label, present in checks.items():
        if present:
            ok(label)
        else:
            fail(label)

    if "analyze_vcd_text" in text:
        print("Route calls: analyze_vcd_text()")

        try:
            from app.simulation.waveform_analyzer import WaveformAnalyzer

            if hasattr(WaveformAnalyzer, "analyze_vcd_text"):
                ok("Analyze route waveform call matches analyzer")
            else:
                fail(
                    "Analyze route waveform call",
                    "analyze_vcd_text() is called but not implemented",
                )
        except Exception as exc:
            fail("Analyze route waveform verification", repr(exc))
else:
    fail("analyze.py exists")

# ---------------------------------------------------------------------------
# 10. DIAGNOSTIC CATALOG
# ---------------------------------------------------------------------------
section("10. REQUIRED DIAGNOSTIC CODES")

diagnostic_expectations = {
    "RIVA1001": "undefined identifier",
    "RIVA3001": "width mismatch",
    "RIVA3002": "signedness mismatch",
    "RIVA6002": "specification mismatch",
}

catalog_files = list((ROOT / "app/diagnostics").rglob("*.py"))

all_catalog_text = "\n".join(
    p.read_text(errors="replace") for p in catalog_files
)

for code, description in diagnostic_expectations.items():
    if code in all_catalog_text:
        ok(code, description)
    else:
        fail(code, f"{description} definition not found")

# ---------------------------------------------------------------------------
# 11. TEST SUITE
# ---------------------------------------------------------------------------
section("11. FULL PYTEST SUITE")

result = subprocess.run(
    [sys.executable, "-m", "pytest", "-q"],
    cwd=ROOT,
    text=True,
    capture_output=True,
)

print(result.stdout[-5000:])

if result.returncode == 0:
    ok("Full pytest suite")
else:
    fail("Full pytest suite", f"exit code {result.returncode}")

# Extract test count
combined = result.stdout + result.stderr

match = re.search(
    r"(\d+)\s+passed(?:,\s+(\d+)\s+skipped)?(?:,\s+(\d+)\s+failed)?",
    combined,
)

if match:
    passed = match.group(1)
    skipped = match.group(2) or "0"
    failed = match.group(3) or "0"
    print(f"Detected: {passed} passed, {skipped} skipped, {failed} failed")

# ---------------------------------------------------------------------------
# 12. REAL API SMOKE
# ---------------------------------------------------------------------------
section("12. REAL API TESTCLIENT SMOKE")

if app:
    try:
        from fastapi.testclient import TestClient

        client = TestClient(app)

        response = client.get("/")

        print("HTTP:", response.status_code)
        print("BODY:", response.json())

        if response.status_code == 200:
            ok("GET /")
        else:
            fail("GET /", str(response.status_code))

    except Exception as exc:
        fail("FastAPI TestClient", f"{type(exc).__name__}: {exc}")

# ---------------------------------------------------------------------------
# 13. REAL CLEAN DESIGN
# ---------------------------------------------------------------------------
section("13. CLEAN DESIGN END-TO-END")

if app:
    try:
        from fastapi.testclient import TestClient

        client = TestClient(app)

        rtl = """
module top (
    input logic [7:0] a,
    input logic [7:0] b,
    output logic [7:0] y
);
assign y = a + b;
endmodule
"""

        spec = """
[REQ-001]
Description: Output shall equal the sum input.
Signal: y
Expected: 8-bit output
"""

        response = client.post(
            "/api/analyze",
            json={
                "rtl_code": rtl,
                "spec_code": spec,
                "testbench_code": "",
                "vcd_content": "",
            },
        )

        print("HTTP:", response.status_code)

        if response.status_code == 200:
            data = response.json()
            diagnostics = data.get("diagnostics", [])

            print("Status:", data.get("status"))
            print("Top:", data.get("top_module"))
            print("Diagnostics:", diagnostics)

            if data.get("status") == "success":
                ok("Clean design API analysis")

            if len(diagnostics) == 0:
                ok("Clean design produces zero diagnostics")
            else:
                fail(
                    "Clean design produces zero diagnostics",
                    str(diagnostics),
                )
        else:
            fail("Clean design API analysis", response.text[:1000])

    except Exception as exc:
        fail("Clean design end-to-end", f"{type(exc).__name__}: {exc}")

# ---------------------------------------------------------------------------
# 14. WIDTH MISMATCH
# ---------------------------------------------------------------------------
section("14. WIDTH MISMATCH END-TO-END")

if app:
    try:
        rtl = """
module top (
    input logic [7:0] a,
    output logic [3:0] y
);
assign y = a;
endmodule
"""

        spec = """
[REQ-001]
Description: Output width.
Signal: y
Expected: 4-bit output
"""

        response = TestClient(app).post(
            "/api/analyze",
            json={
                "rtl_code": rtl,
                "spec_code": spec,
            },
        )

        if response.status_code == 200:
            data = response.json()
            diagnostics = data.get("diagnostics", [])
            codes = [d.get("code") for d in diagnostics]

            print("Codes:", codes)

            if codes.count("RIVA3001") == 1:
                ok("Width mismatch produces exactly one RIVA3001")
            else:
                fail(
                    "Width mismatch diagnostic",
                    f"expected exactly one RIVA3001, got {codes}",
                )

            explanation = data.get("explanation", {})
            findings = explanation.get("findings", [])

            if any(
                f.get("code") == "RIVA3001"
                and "width" in str(f).lower()
                and (
                    "resize" in str(f).lower()
                    or "slice" in str(f).lower()
                    or "extend" in str(f).lower()
                )
                for f in findings
            ):
                ok("AI width explanation/suggestion")
            else:
                fail("AI width explanation/suggestion")
        else:
            fail("Width mismatch API request", response.text[:1000])

    except Exception as exc:
        fail("Width mismatch test", repr(exc))

# ---------------------------------------------------------------------------
# 15. SIGNEDNESS
# ---------------------------------------------------------------------------
section("15. SIGNEDNESS MISMATCH END-TO-END")

if app:
    try:
        rtl = """
module top (
    input logic signed [7:0] a,
    output logic [7:0] y
);
assign y = a;
endmodule
"""

        spec = """
[REQ-001]
Description: Output.
Signal: y
Expected: 8-bit output
"""

        response = TestClient(app).post(
            "/api/analyze",
            json={
                "rtl_code": rtl,
                "spec_code": spec,
            },
        )

        if response.status_code == 200:
            data = response.json()
            diagnostics = data.get("diagnostics", [])
            codes = [d.get("code") for d in diagnostics]

            print("Codes:", codes)

            if codes.count("RIVA3002") == 1:
                ok("Signedness mismatch produces exactly one RIVA3002")
            else:
                fail(
                    "Signedness mismatch diagnostic",
                    f"expected exactly one RIVA3002, got {codes}",
                )

            findings = data.get("explanation", {}).get("findings", [])

            text = " ".join(
                str(f)
                for f in findings
                if f.get("code") == "RIVA3002"
            ).lower()

            if "signed" in text and "unsigned" in text and "cast" in text:
                ok("AI signedness explanation/suggestion")
            else:
                fail("AI signedness explanation/suggestion")
        else:
            fail("Signedness API request", response.text[:1000])

    except Exception as exc:
        fail("Signedness test", repr(exc))

# ---------------------------------------------------------------------------
# 16. UNDEFINED IDENTIFIER
# ---------------------------------------------------------------------------
section("16. UNDEFINED IDENTIFIER END-TO-END")

if app:
    try:
        rtl = """
module top (
    output logic [7:0] y
);
assign y = missing_signal;
endmodule
"""

        spec = """
[REQ-001]
Description: Output.
Signal: y
Expected: 8-bit output
"""

        response = TestClient(app).post(
            "/api/analyze",
            json={
                "rtl_code": rtl,
                "spec_code": spec,
            },
        )

        if response.status_code == 200:
            data = response.json()
            diagnostics = data.get("diagnostics", [])
            codes = [d.get("code") for d in diagnostics]

            print("Codes:", codes)

            if codes.count("RIVA1001") == 1:
                ok("Undefined identifier produces exactly one RIVA1001")
            else:
                fail(
                    "Undefined identifier diagnostic",
                    f"expected exactly one RIVA1001, got {codes}",
                )

            findings = data.get("explanation", {}).get("findings", [])

            text = " ".join(
                str(f)
                for f in findings
                if f.get("code") == "RIVA1001"
            ).lower()

            if "identifier" in text and "declare" in text:
                ok("AI undefined identifier explanation/suggestion")
            else:
                fail("AI undefined identifier explanation/suggestion")
        else:
            fail("Undefined identifier API request", response.text[:1000])

    except Exception as exc:
        fail("Undefined identifier test", repr(exc))

# ---------------------------------------------------------------------------
# 17. SPECIFICATION MISMATCH
# ---------------------------------------------------------------------------
section("17. SPECIFICATION / DESIGN MISMATCH")

if app:
    try:
        rtl = """
module top (
    output logic [7:0] y
);
assign y = 8'h00;
endmodule
"""

        spec = """
[REQ-001]
Description: Required output.
Signal: data_out
Expected: 8-bit output
"""

        response = TestClient(app).post(
            "/api/analyze",
            json={
                "rtl_code": rtl,
                "spec_code": spec,
            },
        )

        if response.status_code == 200:
            data = response.json()

            diagnostics = data.get("diagnostics", [])
            codes = [d.get("code") for d in diagnostics]

            print("Codes:", codes)
            print("Traceability:", data.get("traceability"))

            if "RIVA6002" in codes:
                ok("Specification mismatch produces RIVA6002")
            else:
                fail("Specification mismatch RIVA6002")

            trace = data.get("traceability", [])

            if any(
                x.get("requirement_id") == "REQ-001"
                and x.get("status") == "FAILED"
                for x in trace
            ):
                ok("Failed requirement traceability")
            else:
                fail("Failed requirement traceability")

            findings = data.get("explanation", {}).get("findings", [])

            text = " ".join(
                str(f)
                for f in findings
                if f.get("code") == "RIVA6002"
            ).lower()

            if "requirement" in text and "signal" in text:
                ok("AI specification mismatch explanation")
            else:
                fail("AI specification mismatch explanation")
        else:
            fail("Specification mismatch API request", response.text[:1000])

    except Exception as exc:
        fail("Specification mismatch test", repr(exc))

# ---------------------------------------------------------------------------
# 18. VCD / TESTBENCH
# ---------------------------------------------------------------------------
section("18. TESTBENCH / VCD END-TO-END")

if app:
    try:
        rtl = """
module top (
    input logic clk,
    input logic a,
    output logic y
);
assign y = a;
endmodule
"""

        spec = """
[REQ-001]
Description: Output.
Signal: y
Expected: output follows input
"""

        vcd = """$date
today
$end
$version
RIVA Test
$end
$timescale 1ns $end
$scope module top $end
$var wire 1 ! a $end
$var wire 1 " y $end
$upscope $end
$enddefinitions $end
#0
0!
0"
#10
1!
1"
#20
0!
0"
"""

        response = TestClient(app).post(
            "/api/analyze",
            json={
                "rtl_code": rtl,
                "spec_code": spec,
                "testbench_code": "",
                "vcd_content": vcd,
            },
        )

        print("HTTP:", response.status_code)

        if response.status_code == 200:
            data = response.json()
            print("Waveform:", data.get("waveform"))

            ok("Valid VCD request does not crash")

            if data.get("waveform") not in (None, {}):
                ok("Waveform result returned")
            else:
                warn(
                    "Waveform result empty",
                    "VCD request succeeded but returned no waveform data",
                )

            explanation = data.get("explanation", {})

            if explanation:
                ok("AI explanation survives waveform pipeline")
            else:
                fail("AI explanation after waveform pipeline")

        else:
            fail(
                "Valid VCD request",
                f"HTTP {response.status_code}: {response.text[:1000]}",
            )

    except Exception as exc:
        fail(
            "Valid VCD integration",
            f"{type(exc).__name__}: {exc}",
        )

# ---------------------------------------------------------------------------
# 19. INVALID VCD
# ---------------------------------------------------------------------------
section("19. INVALID VCD ROBUSTNESS")

if app:
    try:
        response = TestClient(app).post(
            "/api/analyze",
            json={
                "rtl_code": """
module top(input logic a, output logic y);
assign y = a;
endmodule
""",
                "spec_code": """
[REQ-001]
Description: Output.
Signal: y
Expected: output
""",
                "vcd_content": "THIS IS NOT A VALID VCD",
            },
        )

        print("HTTP:", response.status_code)

        if response.status_code < 500:
            ok("Malformed VCD does not cause server error")
        else:
            fail(
                "Malformed VCD handling",
                f"HTTP {response.status_code}",
            )

    except Exception as exc:
        fail(
            "Malformed VCD handling",
            f"{type(exc).__name__}: {exc}",
        )

# ---------------------------------------------------------------------------
# 20. AI GROUNDING IMPLEMENTATION
# ---------------------------------------------------------------------------
section("20. AI GROUNDING COMPONENTS")

ai_files = [
    ROOT / "app/ai/evidence_store.py",
    ROOT / "app/ai/grounding_validator.py",
    ROOT / "app/ai/response_validator.py",
    ROOT / "app/ai/ai_reasoning_engine.py",
    ROOT / "app/ai/ai_provider.py",
]

for path in ai_files:
    if path.exists():
        ok("AI component exists", str(path.relative_to(ROOT)))
    else:
        fail("AI component missing", str(path.relative_to(ROOT)))

# ---------------------------------------------------------------------------
# 21. TRACEABILITY
# ---------------------------------------------------------------------------
section("21. TRACEABILITY COMPONENT")

trace_dir = ROOT / "app/analysis/traceability"

if trace_dir.exists():
    files = list(trace_dir.rglob("*.py"))

    if files:
        ok("Traceability implementation exists")
        for p in files:
            print(" ", p.relative_to(ROOT))
    else:
        fail("Traceability implementation empty")
else:
    fail("Traceability directory missing")

# ---------------------------------------------------------------------------
# 22. REPAIR
# ---------------------------------------------------------------------------
section("22. CLOSED-LOOP REPAIR")

repair = ROOT / "app/repair"

if repair.exists():
    files = list(repair.rglob("*.py"))

    if files:
        ok("Repair subsystem exists")
    else:
        fail("Repair subsystem empty")

    closed_loop = repair / "closed_loop_repair.py"

    if closed_loop.exists():
        ok("Closed-loop repair implementation")
    else:
        warn("Closed-loop repair file not found")
else:
    fail("Repair subsystem missing")

# ---------------------------------------------------------------------------
# 23. OPTIMIZATION
# ---------------------------------------------------------------------------
section("23. OPTIMIZATION")

optimization = ROOT / "app/optimization"

if optimization.exists():
    files = list(optimization.rglob("*.py"))

    if files:
        ok("Optimization subsystem exists")
    else:
        fail("Optimization subsystem empty")
else:
    fail("Optimization subsystem missing")

# ---------------------------------------------------------------------------
# 24. SECURITY AUDIT
# ---------------------------------------------------------------------------
section("24. SECURITY / INPUT VALIDATION")

security_patterns = [
    ("path traversal", r"path traversal|directory.*filename|outside.*upload"),
    ("null byte", r"null.*character|\\x00"),
    ("extension validation", r"extension"),
    ("filename validation", r"filename"),
    ("upload rollback", r"rollback|temporary_path"),
]

all_app_text = "\n".join(
    p.read_text(errors="replace")
    for p in (ROOT / "app").rglob("*.py")
)

for label, pattern in security_patterns:
    if re.search(pattern, all_app_text, re.IGNORECASE):
        ok(label)
    else:
        warn(label, "no matching implementation text found")

# ---------------------------------------------------------------------------
# 25. OBSOLETE TYPE RESOLVER
# ---------------------------------------------------------------------------
section("25. OBSOLETE TYPE RESOLVER AUDIT")

old_imports = []

for path in (ROOT / "app").rglob("*.py"):
    text = path.read_text(errors="replace")

    if (
        "from app.semantics.passes.type_resolver import" in text
        or "import app.semantics.passes.type_resolver" in text
    ):
        old_imports.append(str(path.relative_to(ROOT)))

if old_imports:
    fail("Obsolete TypeResolver imports", str(old_imports))
else:
    ok("No obsolete TypeResolver imports")

# ---------------------------------------------------------------------------
# 26. BACKUP FILES
# ---------------------------------------------------------------------------
section("26. BACKUP FILE AUDIT")

backups = list(ROOT.rglob("*.bak"))

if backups:
    fail(
        "Backup files remain",
        ", ".join(str(x.relative_to(ROOT)) for x in backups[:20]),
    )
else:
    ok("No .bak files")

# ---------------------------------------------------------------------------
# 27. DEBUG CODE
# ---------------------------------------------------------------------------
section("27. DEBUG CODE AUDIT")

debug_hits = []

for path in (ROOT / "app").rglob("*.py"):
    text = path.read_text(errors="replace")

    for i, line in enumerate(text.splitlines(), 1):
        if re.search(r"\b(breakpoint|pdb\.set_trace)\s*\(", line):
            debug_hits.append(
                f"{path.relative_to(ROOT)}:{i}: {line.strip()}"
            )

if debug_hits:
    fail("Debugger statements", str(debug_hits[:20]))
else:
    ok("No debugger statements")

# ---------------------------------------------------------------------------
# 28. TODO/FIXME
# ---------------------------------------------------------------------------
section("28. TODO / FIXME AUDIT")

todo_hits = []

for path in (ROOT / "app").rglob("*.py"):
    text = path.read_text(errors="replace")

    for i, line in enumerate(text.splitlines(), 1):
        if re.search(r"\b(TODO|FIXME|XXX)\b", line):
            todo_hits.append(
                f"{path.relative_to(ROOT)}:{i}: {line.strip()}"
            )

if todo_hits:
    warn("TODO/FIXME markers", f"{len(todo_hits)} found")
    for item in todo_hits[:30]:
        print(" ", item)
else:
    ok("No TODO/FIXME/XXX markers")

# ---------------------------------------------------------------------------
# 29. NOTIMPLEMENTED
# ---------------------------------------------------------------------------
section("29. PRODUCTION STUB AUDIT")

not_impl = []

for path in (ROOT / "app").rglob("*.py"):
    text = path.read_text(errors="replace")

    if "raise NotImplementedError" in text:
        not_impl.append(str(path.relative_to(ROOT)))

if not_impl:
    warn(
        "NotImplementedError declarations",
        "Review abstract/base classes versus production paths: "
        + ", ".join(not_impl),
    )
else:
    ok("No NotImplementedError")

# ---------------------------------------------------------------------------
# 30. GIT DIFF
# ---------------------------------------------------------------------------
section("30. GIT DIFF CHECK")

result = subprocess.run(
    ["git", "diff", "--check"],
    cwd=ROOT,
    text=True,
    capture_output=True,
)

if result.returncode == 0:
    ok("git diff --check")
else:
    fail("git diff --check", result.stdout + result.stderr)

# ---------------------------------------------------------------------------
# 31. PYTHON SOURCE COUNT
# ---------------------------------------------------------------------------
section("31. BACKEND SIZE")

source_files = list((ROOT / "app").rglob("*.py"))
test_files = list(ROOT.rglob("test*.py")) + list((ROOT / "tests").rglob("*.py"))

print("Backend Python source files:", len(source_files))
print("Test files:", len(set(test_files)))

if len(source_files) > 0:
    ok("Backend source tree exists")

if len(test_files) > 0:
    ok("Backend test tree exists")

# ---------------------------------------------------------------------------
# 32. FINAL RESULT
# ---------------------------------------------------------------------------
section("FINAL BACKEND AUDIT RESULT")

print(f"PASSED CHECKS : {PASS}")
print(f"FAILED CHECKS : {FAIL}")
print(f"WARNINGS      : {WARN}")

print()
print("WHAT IS COMPLETED:")
print("- Compiler/parser subsystem")
print("- AST")
print("- Semantic analysis")
print("- Type resolution")
print("- Width inference")
print("- Signedness analysis")
print("- Expression analysis")
print("- Assignment compatibility")
print("- Elaboration/hierarchy")
print("- Diagnostics")
print("- CFG/dataflow")
print("- Traceability")
print("- Repair subsystem")
print("- Optimization")
print("- AI/evidence/reporting components")
print("- API/storage components")

print()
print("AREAS REQUIRING SPECIAL ATTENTION:")
print("- WaveformAnalyzer API contract")
print("- Valid VCD end-to-end execution")
print("- Invalid VCD robustness")
print("- Waveform evidence → EvidenceStore")
print("- Waveform evidence → AI grounding")
print("- Project API lifecycle")
print("- Pydantic deprecation warning")

print()

if FAIL == 0:
    print("=" * 78)
    print("RIVA BACKEND AUDIT: PASS")
    print("=" * 78)
    print("No failing checks were detected.")
    print("Review warnings before declaring production-ready.")
else:
    print("=" * 78)
    print("RIVA BACKEND AUDIT: NOT READY")
    print("=" * 78)
    print("Fix every FAIL above, then rerun this exact audit.")

sys.exit(1 if FAIL else 0)
