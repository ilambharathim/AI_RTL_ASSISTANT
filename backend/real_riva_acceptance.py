from fastapi.testclient import TestClient
from app.main import app
import json
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
    print("\n")
    print("=" * 80)
    print(title)
    print("=" * 80)


def analyze(name, rtl, spec, testbench, vcd=""):
    section(name)

    response = client.post(
        "/api/analyze",
        json={
            "rtl_code": rtl,
            "spec_code": spec,
            "testbench_code": testbench,
            "vcd_content": vcd,
        },
    )

    print("HTTP:", response.status_code)

    ok(
        response.status_code == 200,
        f"{name}: HTTP request succeeds",
    )

    if response.status_code != 200:
        print(response.text)
        return None

    data = response.json()

    print("STATUS:", data.get("status"))
    print("TOP MODULE:", data.get("top_module"))

    diagnostics = data.get("diagnostics", [])
    traceability = data.get("traceability", [])
    waveform = data.get("waveform", {})
    explanation = data.get("explanation", {})
    reports = data.get("reports", {})

    print("\nDIAGNOSTICS")

    for d in diagnostics:
        print(
            f"  {d.get('code')} | "
            f"{d.get('severity')} | "
            f"{d.get('category')}"
        )
        print(f"    message   : {d.get('message')}")
        print(f"    suggestion: {d.get('suggestion')}")
        print(f"    location  : {d.get('location')}")

    print("\nTRACEABILITY")

    for t in traceability:
        print(
            f"  {t.get('requirement_id')} | "
            f"{t.get('signal_name')} | "
            f"{t.get('status')}"
        )

    print("\nWAVEFORM")
    print(json.dumps(waveform, indent=2))

    print("\nAI EXPLANATION")
    print(json.dumps(explanation, indent=2))

    print("\nREPORTS")
    print("  markdown:", bool(reports.get("markdown")))
    print("  json    :", bool(reports.get("json")))

    return data


# =============================================================================
# COMMON SPECIFICATION
# =============================================================================

CLEAN_SPEC = """
[REQ-001]
Category: FUNCTIONAL
Signal: y
Description: The output y shall equal the sum of inputs a and b.
Expected: y = a + b
"""


CLEAN_TB = """
module top_tb;

    logic [7:0] a;
    logic [7:0] b;
    logic [7:0] y;

    top dut (
        .a(a),
        .b(b),
        .y(y)
    );

    initial begin
        a = 8'd10;
        b = 8'd20;
        #10;

        if (y !== 8'd30)
            $error("Incorrect addition result");

        a = 8'd100;
        b = 8'd20;
        #10;

        if (y !== 8'd120)
            $error("Incorrect addition result");

        $finish;
    end

endmodule
"""


CLEAN_RTL = """
module top (
    input  logic [7:0] a,
    input  logic [7:0] b,
    output logic [7:0] y
);

    assign y = a + b;

endmodule
"""


# =============================================================================
# TEST 1 — CLEAN REAL DESIGN
# =============================================================================

clean = analyze(
    "TEST 1 — CLEAN SYSTEMVERILOG + SPEC + TESTBENCH",
    CLEAN_RTL,
    CLEAN_SPEC,
    CLEAN_TB,
)

if clean:
    clean_codes = [
        d.get("code")
        for d in clean.get("diagnostics", [])
    ]

    ok(
        clean.get("status") == "success",
        "Clean design status is success",
    )

    ok(
        len(clean_codes) == 0,
        "Clean design produces ZERO diagnostics",
    )

    ok(
        "RIVA1001" not in clean_codes,
        "Clean design does not fabricate undefined identifier",
    )

    ok(
        "RIVA3001" not in clean_codes,
        "Clean design does not fabricate width mismatch",
    )

    ok(
        "RIVA3002" not in clean_codes,
        "Clean design does not fabricate signedness mismatch",
    )

    ok(
        "RIVA6002" not in clean_codes,
        "Clean design does not fabricate specification mismatch",
    )

    trace = clean.get("traceability", [])

    ok(
        any(
            t.get("requirement_id") == "REQ-001"
            and t.get("status") == "PASSED"
            for t in trace
        ),
        "Clean requirement passes traceability",
    )

    ok(
        bool(clean.get("reports", {}).get("markdown")),
        "Clean design generates Markdown report",
    )

    ok(
        bool(clean.get("reports", {}).get("json")),
        "Clean design generates JSON report",
    )


# =============================================================================
# TEST 2 — REAL WIDTH ERROR
# =============================================================================

WIDTH_RTL = """
module top (
    input  logic [7:0] a,
    input  logic [7:0] b,
    output logic [3:0] y
);

    assign y = a + b;

endmodule
"""

width = analyze(
    "TEST 2 — REAL RTL WIDTH MISMATCH",
    WIDTH_RTL,
    CLEAN_SPEC,
    CLEAN_TB,
)

if width:
    codes = [
        d.get("code")
        for d in width.get("diagnostics", [])
    ]

    ok(
        "RIVA3001" in codes,
        "Width mismatch produces RIVA3001",
    )

    width_diag = next(
        (
            d
            for d in width.get("diagnostics", [])
            if d.get("code") == "RIVA3001"
        ),
        None,
    )

    ok(
        width_diag is not None,
        "RIVA3001 diagnostic contains evidence",
    )

    if width_diag:
        suggestion = (
            width_diag.get("suggestion", "")
            .lower()
        )

        ok(
            "resize" in suggestion
            or "slice" in suggestion
            or "extend" in suggestion,
            "Width diagnostic provides a technically relevant fix",
        )

    ai = json.dumps(
        width.get("explanation", {})
    ).lower()

    ok(
        "riva3001" in ai,
        "AI explanation references RIVA3001",
    )

    ok(
        "width" in ai,
        "AI explains the width problem",
    )

    ok(
        "resize" in ai
        or "slice" in ai
        or "extend" in ai,
        "AI suggests an appropriate width correction",
    )

    ok(
        "signedness" not in ai,
        "Width error is not incorrectly explained as signedness",
    )


# =============================================================================
# TEST 3 — REAL SIGNEDNESS ERROR
# =============================================================================

SIGNED_RTL = """
module top (
    input logic signed [7:0] a,
    output logic [7:0] y
);

    assign y = a;

endmodule
"""

SIGNED_SPEC = """
[REQ-001]
Category: FUNCTIONAL
Signal: y
Description: Output y shall carry the value of input a.
Expected: 8-bit output
"""

signedness = analyze(
    "TEST 3 — REAL SIGNEDNESS MISMATCH",
    SIGNED_RTL,
    SIGNED_SPEC,
    "",
)

if signedness:
    codes = [
        d.get("code")
        for d in signedness.get("diagnostics", [])
    ]

    ok(
        "RIVA3002" in codes,
        "Signedness mismatch produces RIVA3002",
    )

    ai = json.dumps(
        signedness.get("explanation", {})
    ).lower()

    ok(
        "riva3002" in ai,
        "AI explanation references RIVA3002",
    )

    ok(
        "signed" in ai and "unsigned" in ai,
        "AI correctly explains signed/unsigned mismatch",
    )

    ok(
        "cast" in ai
        or "signedness" in ai
        or "matching" in ai,
        "AI provides a relevant signedness correction",
    )


# =============================================================================
# TEST 4 — REAL UNDEFINED SIGNAL
# =============================================================================

UNDEFINED_RTL = """
module top (
    input logic [7:0] a,
    output logic [7:0] y
);

    assign y = missing_signal;

endmodule
"""

undefined = analyze(
    "TEST 4 — REAL UNDEFINED SIGNAL",
    UNDEFINED_RTL,
    CLEAN_SPEC,
    "",
)

if undefined:
    codes = [
        d.get("code")
        for d in undefined.get("diagnostics", [])
    ]

    ok(
        "RIVA1001" in codes,
        "Undefined signal produces RIVA1001",
    )

    diag = next(
        (
            d
            for d in undefined.get("diagnostics", [])
            if d.get("code") == "RIVA1001"
        ),
        None,
    )

    if diag:
        ok(
            "missing_signal" in diag.get("message", ""),
            "Diagnostic identifies the actual missing signal",
        )

        ok(
            "declare" in diag.get("suggestion", "").lower()
            or "spelling" in diag.get("suggestion", "").lower(),
            "Undefined signal provides relevant correction",
        )

    ai = json.dumps(
        undefined.get("explanation", {})
    ).lower()

    ok(
        "missing_signal" in ai,
        "AI identifies the actual undefined signal",
    )

    ok(
        "declare" in ai
        or "spelling" in ai,
        "AI suggests declaration or spelling correction",
    )


# =============================================================================
# TEST 5 — SPECIFICATION / DESIGN MISMATCH
# =============================================================================

MISMATCH_SPEC = """
[REQ-001]
Category: FUNCTIONAL
Signal: data_out
Description: The module shall provide the processed output on data_out.
Expected: 8-bit output
"""

SPEC_MISMATCH_RTL = """
module top (
    input logic [7:0] a,
    output logic [7:0] y
);

    assign y = a;

endmodule
"""

spec_mismatch = analyze(
    "TEST 5 — SPECIFICATION / DESIGN MISMATCH",
    SPEC_MISMATCH_RTL,
    MISMATCH_SPEC,
    "",
)

if spec_mismatch:
    codes = [
        d.get("code")
        for d in spec_mismatch.get("diagnostics", [])
    ]

    ok(
        "RIVA6002" in codes,
        "Specification mismatch produces RIVA6002",
    )

    trace = spec_mismatch.get(
        "traceability",
        []
    )

    ok(
        any(
            t.get("requirement_id") == "REQ-001"
            and t.get("status") == "FAILED"
            for t in trace
        ),
        "Failed specification requirement is traceable",
    )

    ai = json.dumps(
        spec_mismatch.get("explanation", {})
    ).lower()

    ok(
        "data_out" in ai,
        "AI identifies the actual specification signal",
    )

    ok(
        "requirement" in ai,
        "AI explains the requirement failure",
    )

    ok(
        "declare" in ai
        or "align" in ai
        or "implementation" in ai,
        "AI provides a relevant specification correction",
    )


# =============================================================================
# TEST 6 — TESTBENCH / WAVEFORM
# =============================================================================

VCD = """
$timescale 1ns $end
$scope module top $end
$var wire 8 ! a [7:0] $end
$var wire 8 " y [7:0] $end
$upscope $end
$enddefinitions $end

#0
b00001010 !
b00001010 "

#10
b00010100 !
b00011110 "

#20
b01100100 !
b01111000 "
"""

waveform = analyze(
    "TEST 6 — TESTBENCH + VCD WAVEFORM",
    CLEAN_RTL,
    CLEAN_SPEC,
    CLEAN_TB,
    VCD,
)

if waveform:
    wf = waveform.get("waveform", {})

    print("\nWAVEFORM EVENTS:", wf.get("events_count"))
    print("SIGNALS:", wf.get("signals_analyzed"))

    ok(
        isinstance(wf, dict),
        "Waveform result is returned",
    )

    ok(
        wf.get("status") == "success",
        "VCD analysis succeeds",
    )

    ok(
        wf.get("events_count", 0) > 0,
        "VCD contains parsed waveform events",
    )

    signals = wf.get(
        "signals_analyzed",
        [],
    )

    ok(
        "a" in signals and "y" in signals,
        "VCD analyzer recognizes expected signals",
    )

    evidence_text = json.dumps(
        waveform.get("explanation", {})
    ).lower()

    ok(
        "waveform" in evidence_text
        or "vcd" in evidence_text
        or waveform.get("waveform") is not None,
        "Waveform evidence survives the analysis pipeline",
    )


# =============================================================================
# TEST 7 — BAD TESTBENCH / INVALID VCD
# =============================================================================

BAD_VCD = """
THIS IS NOT A VALID VCD FILE
#invalid_time
random garbage
$broken
"""

bad_vcd = analyze(
    "TEST 7 — INVALID TESTBENCH / MALFORMED VCD",
    CLEAN_RTL,
    CLEAN_SPEC,
    """
    module broken_tb;
        initial begin
            unknown_signal = 1'b1;
        end
    endmodule
    """,
    BAD_VCD,
)

if bad_vcd:
    ok(
        True,
        "Malformed VCD does not crash the API",
    )

    ok(
        bad_vcd.get("status") == "success",
        "Malformed VCD is handled without server failure",
    )


# =============================================================================
# TEST 8 — CLEAN EXPRESSION REGRESSION
# =============================================================================

EXPRESSION_RTL = """
module top (
    input logic [7:0] a,
    input logic [7:0] b,
    output logic [7:0] y
);

    assign y = a + b;

endmodule
"""

expression = analyze(
    "TEST 8 — BINARY EXPRESSION REGRESSION",
    EXPRESSION_RTL,
    CLEAN_SPEC,
    "",
)

if expression:
    codes = [
        d.get("code")
        for d in expression.get("diagnostics", [])
    ]

    ok(
        "RIVA1001" not in codes,
        "Binary expression does not become a false undefined identifier",
    )

    ok(
        "RIVA6002" not in codes,
        "Requirement parser does not fabricate a false target",
    )


# =============================================================================
# FINAL RESULT
# =============================================================================

section("FINAL RIVA REAL-CODE ACCEPTANCE RESULT")

print(f"PASSED CHECKS : {PASS}")
print(f"FAILED CHECKS : {FAIL}")

print()

if FAIL == 0:
    print("=" * 80)
    print("RIVA BACKEND ACCEPTANCE: PASS")
    print("=" * 80)
    print()
    print("The backend successfully handled:")
    print("  ✓ Clean SystemVerilog")
    print("  ✓ Clean specification")
    print("  ✓ Real testbench")
    print("  ✓ Width mismatch")
    print("  ✓ Signedness mismatch")
    print("  ✓ Undefined signal")
    print("  ✓ Specification/design mismatch")
    print("  ✓ VCD waveform analysis")
    print("  ✓ Malformed VCD")
    print("  ✓ Expression parsing")
    print("  ✓ Requirement traceability")
    print("  ✓ Diagnostic codes")
    print("  ✓ AI explanations")
    print("  ✓ AI suggestions")
    print("  ✓ Reports")
    print()
    print("BACKEND IS READY FOR FRONTEND INTEGRATION.")
    sys.exit(0)

else:
    print("=" * 80)
    print("RIVA BACKEND ACCEPTANCE: FAILED")
    print("=" * 80)
    print()
    print("DO NOT modify the frontend.")
    print("Fix the failed backend scenarios above first.")
    sys.exit(1)
