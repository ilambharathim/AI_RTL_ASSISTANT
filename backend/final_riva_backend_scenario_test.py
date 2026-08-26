from fastapi.testclient import TestClient
from app.main import app
import json
import re
import sys

client = TestClient(app)

PASS = 0
FAIL = 0


def ok(condition, message):
    global PASS, FAIL
    if condition:
        print(f"PASS  {message}")
        PASS += 1
    else:
        print(f"FAIL  {message}")
        FAIL += 1


def section(title):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def show_response(response):
    print("HTTP:", response.status_code)

    try:
        data = response.json()
    except Exception:
        print(response.text)
        return None

    print("STATUS:", data.get("status"))
    print("TOP MODULE:", data.get("top_module"))

    print("\nDIAGNOSTICS:")
    for d in data.get("diagnostics", []):
        print(
            f"  {d.get('code')} | "
            f"{d.get('severity')} | "
            f"{d.get('category')} | "
            f"{d.get('message')}"
        )
        print(f"     suggestion: {d.get('suggestion')}")
        print(f"     location  : {d.get('location')}")

    print("\nTRACEABILITY:")
    for t in data.get("traceability", []):
        print(" ", t)

    print("\nAI EXPLANATION:")
    print(json.dumps(data.get("explanation"), indent=2))

    print("\nREPORT:")
    reports = data.get("reports", {})
    print(" markdown:", bool(reports.get("markdown")))
    print(" json    :", bool(reports.get("json")))

    return data


def diagnostic_codes(data):
    return [str(x.get("code")) for x in data.get("diagnostics", [])]


def ai_findings(data):
    explanation = data.get("explanation") or {}
    return explanation.get("findings", [])


def verify_ai_for_code(data, code, required_words):
    findings = ai_findings(data)

    matching = [
        f for f in findings
        if str(f.get("code", "")).upper() == code.upper()
    ]

    ok(
        len(matching) >= 1,
        f"AI contains explanation for {code}"
    )

    if not matching:
        return

    text = json.dumps(matching[0]).lower()

    for word in required_words:
        ok(
            word.lower() in text,
            f"AI explanation for {code} contains '{word}'"
        )


# ======================================================================
# TEST 1 — CLEAN DESIGN
# ======================================================================

section("TEST 1 — CLEAN RTL DESIGN")

clean_rtl = r"""
module top (
    input logic [7:0] a,
    input logic [7:0] b,
    output logic [7:0] y
);

assign y = a + b;

endmodule
"""

clean_spec = r"""
[REQ-001]
Description: Output y shall be an 8-bit result.
Signal: y
Expected: 8-bit output
Category: FUNCTIONAL
"""

response = client.post(
    "/api/analyze",
    json={
        "rtl_code": clean_rtl,
        "spec_code": clean_spec,
        "testbench_code": "",
        "vcd_content": "",
    },
)

data = show_response(response)

ok(response.status_code == 200, "Clean design HTTP request succeeds")
ok(data is not None, "Clean design returns JSON")
ok(data.get("status") == "success", "Clean design status is success")

codes = diagnostic_codes(data)

print("\nCLEAN DESIGN CODES:", codes)

bad_clean_codes = {
    "RIVA1001",
    "RIVA3001",
    "RIVA3002",
    "RIVA6002",
}

for code in bad_clean_codes:
    ok(
        code not in codes,
        f"Clean design does not fabricate {code}"
    )

ok(
    len(codes) == 0,
    "Clean design produces ZERO diagnostics"
)


# ======================================================================
# TEST 2 — REAL RTL DESIGN ERROR
# ======================================================================

section("TEST 2 — RTL WIDTH MISMATCH")

width_error_rtl = r"""
module top (
    input logic [7:0] a,
    output logic [3:0] y
);

assign y = a;

endmodule
"""

width_spec = r"""
[REQ-001]
Description: Output y shall be 4 bits.
Signal: y
Expected: 4-bit output
Category: FUNCTIONAL
"""

response = client.post(
    "/api/analyze",
    json={
        "rtl_code": width_error_rtl,
        "spec_code": width_spec,
        "testbench_code": "",
        "vcd_content": "",
    },
)

data = show_response(response)

ok(response.status_code == 200, "Width-error request succeeds")

codes = diagnostic_codes(data)

print("\nWIDTH ERROR CODES:", codes)

ok(
    "RIVA3001" in codes,
    "Width mismatch produces RIVA3001"
)

ok(
    codes.count("RIVA3001") == 1,
    "Width mismatch produces exactly ONE RIVA3001"
)

verify_ai_for_code(
    data,
    "RIVA3001",
    [
        "width",
        "resize",
    ],
)

# Check that AI does not explain it as an unrelated error.
ai_text = json.dumps(data.get("explanation", {})).lower()

ok(
    "signedness mismatch" not in ai_text,
    "Width-error AI does not misclassify the problem as signedness"
)


# ======================================================================
# TEST 3 — SIGNEDNESS / RTL DESIGN ERROR
# ======================================================================

section("TEST 3 — RTL SIGNEDNESS MISMATCH")

signedness_rtl = r"""
module top (
    input logic signed [7:0] a,
    output logic [7:0] y
);

assign y = a;

endmodule
"""

signedness_spec = r"""
[REQ-001]
Description: Output y shall be 8 bits.
Signal: y
Expected: 8-bit output
Category: FUNCTIONAL
"""

response = client.post(
    "/api/analyze",
    json={
        "rtl_code": signedness_rtl,
        "spec_code": signedness_spec,
        "testbench_code": "",
        "vcd_content": "",
    },
)

data = show_response(response)

ok(response.status_code == 200, "Signedness-error request succeeds")

codes = diagnostic_codes(data)

print("\nSIGNEDNESS ERROR CODES:", codes)

ok(
    "RIVA3002" in codes,
    "Signedness mismatch produces RIVA3002"
)

ok(
    codes.count("RIVA3002") == 1,
    "Signedness mismatch produces exactly ONE RIVA3002"
)

verify_ai_for_code(
    data,
    "RIVA3002",
    [
        "signed",
        "unsigned",
        "cast",
    ],
)


# ======================================================================
# TEST 4 — UNDEFINED SIGNAL
# ======================================================================

section("TEST 4 — UNDEFINED SIGNAL")

undefined_rtl = r"""
module top (
    input logic [7:0] a,
    output logic [7:0] y
);

assign y = missing_signal;

endmodule
"""

undefined_spec = r"""
[REQ-001]
Description: Output y shall be an 8-bit result.
Signal: y
Expected: 8-bit output
Category: FUNCTIONAL
"""

response = client.post(
    "/api/analyze",
    json={
        "rtl_code": undefined_rtl,
        "spec_code": undefined_spec,
        "testbench_code": "",
        "vcd_content": "",
    },
)

data = show_response(response)

ok(response.status_code == 200, "Undefined-signal request succeeds")

codes = diagnostic_codes(data)

print("\nUNDEFINED SIGNAL CODES:", codes)

ok(
    "RIVA1001" in codes,
    "Undefined signal produces RIVA1001"
)

ok(
    codes.count("RIVA1001") == 1,
    "Undefined signal produces exactly ONE RIVA1001"
)

verify_ai_for_code(
    data,
    "RIVA1001",
    [
        "identifier",
        "declare",
    ],
)


# ======================================================================
# TEST 5 — SPECIFICATION ↔ RTL MISMATCH
# ======================================================================

section("TEST 5 — SPECIFICATION / DESIGN MISMATCH")

spec_mismatch_rtl = r"""
module top (
    input logic [7:0] a,
    output logic [7:0] y
);

assign y = a;

endmodule
"""

spec_mismatch = r"""
[REQ-001]
Description: The output data_out shall be 16 bits.
Signal: data_out
Expected: 16-bit output
Category: FUNCTIONAL
"""

response = client.post(
    "/api/analyze",
    json={
        "rtl_code": spec_mismatch_rtl,
        "spec_code": spec_mismatch,
        "testbench_code": "",
        "vcd_content": "",
    },
)

data = show_response(response)

ok(
    response.status_code == 200,
    "Specification mismatch request succeeds"
)

codes = diagnostic_codes(data)

print("\nSPECIFICATION MISMATCH CODES:", codes)

ok(
    "RIVA6002" in codes or "SPEC_MISMATCH" in codes,
    "Specification mismatch is detected"
)

traceability = data.get("traceability", [])

ok(
    len(traceability) >= 1,
    "Traceability result is returned"
)

verify_ai_for_code(
    data,
    "RIVA6002",
    [
        "requirement",
        "signal",
    ],
)

# Ensure AI talks about data_out rather than inventing another target.
ai_text = json.dumps(data.get("explanation", {})).lower()

ok(
    "data_out" in ai_text or "requirement" in ai_text,
    "AI explanation references the actual specification evidence"
)


# ======================================================================
# TEST 6 — TESTBENCH / WAVEFORM ERROR
# ======================================================================

section("TEST 6 — TESTBENCH / WAVEFORM VERIFICATION")

# Minimal VCD containing a signal whose observed value changes.
# The exact semantic interpretation is intentionally delegated to
# RIVA's waveform analyzer.

vcd = r"""
$date
    today
$end
$version
    RIVA verification test
$end
$timescale 1ns $end
$scope module top $end
$var wire 1 ! y $end
$upscope $end
$enddefinitions $end

#0
0!

#10
1!

#20
0!

"""

testbench = r"""
module tb;

logic [7:0] a;
logic [7:0] b;
logic [7:0] y;

top dut (
    .a(a),
    .b(b),
    .y(y)
);

initial begin
    a = 8'h00;
    b = 8'h00;

    #10;
    a = 8'h01;

    #10;
    $finish;
end

endmodule
"""

response = client.post(
    "/api/analyze",
    json={
        "rtl_code": clean_rtl,
        "spec_code": clean_spec,
        "testbench_code": testbench,
        "vcd_content": vcd,
    },
)

data = show_response(response)

ok(
    response.status_code == 200,
    "Testbench/waveform request succeeds"
)

waveform = data.get("waveform")

ok(
    waveform is not None,
    "Waveform analysis result exists"
)

print("\nWAVEFORM RESULT:")
print(json.dumps(waveform, indent=2))

ok(
    isinstance(waveform, dict),
    "Waveform result has structured representation"
)


# ======================================================================
# TEST 7 — AI HALLUCINATION SAFETY
# ======================================================================

section("TEST 7 — AI GROUNDING / HALLUCINATION SAFETY")

for label, data in [
    ("CLEAN", client.post(
        "/api/analyze",
        json={
            "rtl_code": clean_rtl,
            "spec_code": clean_spec,
            "testbench_code": "",
            "vcd_content": "",
        },
    ).json()),
    ("WIDTH", client.post(
        "/api/analyze",
        json={
            "rtl_code": width_error_rtl,
            "spec_code": width_spec,
            "testbench_code": "",
            "vcd_content": "",
        },
    ).json()),
    ("UNDEFINED", client.post(
        "/api/analyze",
        json={
            "rtl_code": undefined_rtl,
            "spec_code": undefined_spec,
            "testbench_code": "",
            "vcd_content": "",
        },
    ).json()),
]:

    codes = {
        c.lower()
        for c in diagnostic_codes(data)
    }

    explanation = json.dumps(
        data.get("explanation", {})
    ).lower()

    print(f"\n{label}")
    print("Evidence codes:", sorted(codes))

    # AI must not claim diagnostic codes that aren't in deterministic evidence.
    ai_codes = set(
        re.findall(
            r"\bRIVA\d{4}\b",
            explanation.upper()
        )
    )

    unsupported = {
        c.lower()
        for c in ai_codes
        if c.lower() not in codes
    }

    print("AI codes:", sorted(ai_codes))
    print("Unsupported AI codes:", sorted(unsupported))

    ok(
        not unsupported,
        f"{label}: AI does not invent unsupported RIVA diagnostic codes"
    )

    ok(
        bool(data.get("explanation")),
        f"{label}: AI explanation exists"
    )


# ======================================================================
# TEST 8 — REPORTING
# ======================================================================

section("TEST 8 — REPORT COMPLETENESS")

for label, data in [
    ("CLEAN", client.post(
        "/api/analyze",
        json={
            "rtl_code": clean_rtl,
            "spec_code": clean_spec,
        },
    ).json()),

    ("WIDTH", client.post(
        "/api/analyze",
        json={
            "rtl_code": width_error_rtl,
            "spec_code": width_spec,
        },
    ).json()),
]:

    reports = data.get("reports", {})

    ok(
        bool(reports.get("markdown")),
        f"{label}: Markdown report generated"
    )

    ok(
        bool(reports.get("json")),
        f"{label}: JSON report generated"
    )


def run_all_scenarios():
    section("FINAL RIVA BACKEND SCENARIO RESULT")

    print("PASSED:", PASS)
    print("FAILED:", FAIL)

    if FAIL == 0:
        print()
        print("=" * 80)
        print("RIVA BACKEND SCENARIO VERIFICATION: PASS")
        print("=" * 80)
        print()
        print("All tested backend scenarios passed.")
        print("Frontend was NOT tested or modified.")
        sys.exit(0)
    else:
        print()
        print("=" * 80)
        print("RIVA BACKEND SCENARIO VERIFICATION: FAIL")
        print("=" * 80)
        print()
        print("Fix the failed backend scenarios before declaring RIVA complete.")
        sys.exit(1)


if __name__ == "__main__":
    run_all_scenarios()

