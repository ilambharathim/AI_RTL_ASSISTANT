#!/usr/bin/env bash

set -u

PASS=0
FAIL=0

pass() {
    echo "PASS  $1"
    PASS=$((PASS + 1))
}

fail() {
    echo "FAIL  $1"
    FAIL=$((FAIL + 1))
}

echo "======================================================================"
echo "                 RIVA FINAL BACKEND VERIFICATION"
echo "======================================================================"

echo
echo "===== 1. LOCATION ====="
pwd

if [[ "$(pwd)" == "$HOME/RIVA/backend" ]]; then
    pass "Backend working directory"
else
    fail "Backend working directory"
fi

echo
echo "===== 2. GIT BRANCH ====="
git branch --show-current

echo
echo "===== 3. PYTHON VERSION ====="
python --version

echo
echo "===== 4. PYTHON COMPILE ====="
if PYTHONPATH=. python -m compileall -q app; then
    pass "Python compilation"
else
    fail "Python compilation"
fi

echo
echo "===== 5. CORE MODULE IMPORT AUDIT ====="

PYTHONPATH=. python - <<'PY'
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

failed = False

for name, module in modules:
    try:
        __import__(module)
        print(f"PASS  {name:28} {module}")
    except Exception as exc:
        print(f"FAIL  {name:28} {module}")
        print(f"      {type(exc).__name__}: {exc}")
        failed = True

raise SystemExit(1 if failed else 0)
PY

if [[ $? -eq 0 ]]; then
    pass "Core module imports"
else
    fail "Core module imports"
fi

echo
echo "===== 6. FASTAPI APPLICATION IMPORT ====="

PYTHONPATH=. python - <<'PY'
from app.main import app

print("PASS  FastAPI application import")
print("Title :", app.title)
print("Version:", app.version)
PY

if [[ $? -eq 0 ]]; then
    pass "FastAPI application"
else
    fail "FastAPI application"
fi

echo
echo "===== 7. ACTUAL REGISTERED ROUTES ====="

PYTHONPATH=. python - <<'PY'
from app.main import app

print("REGISTERED ROUTES")

for route in app.routes:
    path = getattr(route, "path", None)
    methods = getattr(route, "methods", None)

    if path and methods:
        print(f"{','.join(sorted(methods)):15} {path}")

print()
print("OPENAPI PATHS")

for path, operations in app.openapi()["paths"].items():
    print(f"{path:40} {','.join(sorted(operations.keys()))}")
PY

echo
echo "===== 8. REQUIRED API ROUTE CHECK ====="

PYTHONPATH=. python - <<'PY'
from app.main import app

required = {
    ("GET", "/"),
    ("POST", "/upload"),
    ("POST", "/api/upload"),
    ("POST", "/api/analyze"),
    ("POST", "/api/projects"),
    ("POST", "/api/projects/{project_id}/files"),
    ("GET", "/api/projects/{project_id}/status"),
}

actual = set()

for route in app.routes:
    path = getattr(route, "path", None)
    methods = getattr(route, "methods", None)

    if path and methods:
        for method in methods:
            actual.add((method, path))

missing = required - actual

if missing:
    print("MISSING ROUTES:")
    for item in sorted(missing):
        print(" ", item)
    raise SystemExit(1)

print("PASS  All required backend routes are registered")
PY

if [[ $? -eq 0 ]]; then
    pass "Required API routes"
else
    fail "Required API routes"
fi

echo
echo "===== 9. OPENAPI ROUTE CHECK ====="

PYTHONPATH=. python - <<'PY'
from app.main import app

required = [
    "/upload",
    "/api/upload",
    "/api/analyze",
    "/api/projects",
    "/api/projects/{project_id}/files",
    "/api/projects/{project_id}/status",
]

paths = app.openapi()["paths"]

missing = [p for p in required if p not in paths]

if missing:
    print("Missing OpenAPI paths:")
    for p in missing:
        print(" ", p)
    raise SystemExit(1)

print("PASS  Required routes exposed through OpenAPI")
PY

if [[ $? -eq 0 ]]; then
    pass "OpenAPI routes"
else
    fail "OpenAPI routes"
fi

echo
echo "===== 10. FULL TEST SUITE ====="

PYTHONPATH=. pytest -q
TEST_STATUS=$?

if [[ $TEST_STATUS -eq 0 ]]; then
    pass "Full pytest suite"
else
    fail "Full pytest suite"
fi

echo
echo "===== 11. TEST COUNT ====="

PYTHONPATH=. pytest --collect-only -q 2>/dev/null | tail -n 5

echo
echo "===== 12. OBSOLETE TYPE RESOLVER IMPORT AUDIT ====="

if grep -RIn \
    --exclude-dir='__pycache__' \
    --exclude='*.bak' \
    -E \
    'from app\.semantics\.passes\.type_resolver|import app\.semantics\.passes\.type_resolver' \
    app test_*.py tests 2>/dev/null; then

    fail "Obsolete TypeResolver imports found"
else
    pass "No obsolete TypeResolver imports"
fi

echo
echo "===== 13. DEBUG CODE AUDIT ====="

DEBUG_FOUND=0

if grep -RIn \
    --exclude-dir='__pycache__' \
    --exclude='*.bak' \
    -E \
    'breakpoint\(\)|pdb\.set_trace\(\)|ipdb\.set_trace\(\)' \
    app 2>/dev/null; then
    DEBUG_FOUND=1
fi

if [[ $DEBUG_FOUND -eq 0 ]]; then
    pass "No debugger statements"
else
    fail "Debugger statements found"
fi

echo
echo "===== 14. TODO / FIXME AUDIT ====="

TODO_FOUND=0

if grep -RIn \
    --exclude-dir='__pycache__' \
    --exclude='*.bak' \
    -E \
    'TODO|FIXME|XXX' \
    app 2>/dev/null; then
    TODO_FOUND=1
fi

if [[ $TODO_FOUND -eq 0 ]]; then
    pass "No TODO/FIXME/XXX markers"
else
    fail "TODO/FIXME/XXX markers found"
fi

echo
echo "===== 15. BACKUP FILE AUDIT ====="

BACKUPS=$(find app tests -type f \
    \( -name '*.bak' -o -name '*.backup' -o -name '*~' \) \
    2>/dev/null)

if [[ -z "$BACKUPS" ]]; then
    pass "No backup files"
else
    echo "$BACKUPS"
    fail "Backup files found"
fi

echo
echo "===== 16. CACHE AUDIT ====="

CACHE_COUNT=$(find app tests -type d -name '__pycache__' 2>/dev/null | wc -l)

echo "Found $CACHE_COUNT __pycache__ directories"

echo
echo "===== 17. GIT DIFF CHECK ====="

if git diff --check; then
    pass "git diff --check"
else
    fail "git diff --check"
fi

echo
echo "===== 18. BACKEND FILE COUNTS ====="

echo "Python source files:"
find app -type f -name '*.py' | wc -l

echo
echo "Test files:"
find . -type f -name 'test_*.py' | wc -l

echo
echo "===== 19. API TESTCLIENT SMOKE ====="

PYTHONPATH=. python - <<'PY'
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

response = client.get("/")

print("Status:", response.status_code)
print("Body  :", response.json())

if response.status_code != 200:
    raise SystemExit(1)

print("PASS  API root TestClient request")
PY

if [[ $? -eq 0 ]]; then
    pass "API TestClient smoke test"
else
    fail "API TestClient smoke test"
fi

echo
echo "===== 20. BACKEND DIRECTORY CHECK ====="

if [[ -d app/ai &&
      -d app/analysis &&
      -d app/diagnostics &&
      -d app/elaboration &&
      -d app/ir &&
      -d app/optimization &&
      -d app/parsers &&
      -d app/repair &&
      -d app/reporting &&
      -d app/semantics &&
      -d app/simulation &&
      -d app/storage &&
      -d app/api ]]; then

    pass "Required backend subsystems exist"
else
    fail "Required backend subsystem missing"
fi

echo
echo "======================================================================"
echo "                     FINAL BACKEND RESULT"
echo "======================================================================"

echo "PASSED CHECKS : $PASS"
echo "FAILED CHECKS : $FAIL"

if [[ $FAIL -eq 0 ]]; then
    echo
    echo "============================================================"
    echo "                  BACKEND VERIFICATION PASS"
    echo "============================================================"
    echo
    echo "RIVA BACKEND STATUS: READY"
    echo
    echo "No frontend verification was performed."
    echo "No frontend files were modified by this audit."
    echo
    exit 0
else
    echo
    echo "============================================================"
    echo "                  BACKEND VERIFICATION FAILED"
    echo "============================================================"
    echo
    echo "RIVA BACKEND STATUS: NOT READY"
    echo
    exit 1
fi
