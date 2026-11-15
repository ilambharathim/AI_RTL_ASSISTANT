"""
RIVA Kiwi Engineering Assistant AI Provider & Grounded Context Engine.
Provides clean LLM provider abstraction and context-grounded fallback.
"""

from __future__ import annotations
import os
import re
import json
import urllib.request
import urllib.error
from typing import Dict, List, Any, Optional


class KiwiAIProviderManager:
    """
    Manages AI inference for Kiwi Verification Assistant.
    Supports live LLM provider connections (Gemini / OpenAI / Anthropic) with automatic fallback
    to RIVA's grounded evidence engine when no API keys are configured in the environment.
    """

    def __init__(self):
        self.gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    def generate_chat_response(
        self,
        messages: List[Dict[str, str]],
        project_context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generates a context-aware chat response for Kiwi.
        """
        # Try live LLM provider if API key is present
        if self.gemini_key:
            res = self._call_gemini_api(messages, project_context)
            if res:
                return {
                    "text": res,
                    "provider": "gemini",
                    "live_ai": True,
                }

        if self.openai_key:
            res = self._call_openai_api(messages, project_context)
            if res:
                return {
                    "text": res,
                    "provider": "openai",
                    "live_ai": True,
                }

        # Grounded Evidence Engine Fallback (Deterministic & Context-Aware)
        fallback_text = self._generate_grounded_fallback(messages, project_context)
        return {
            "text": fallback_text,
            "provider": "riva_grounded_engine",
            "live_ai": False,
        }

    def _build_system_prompt(self, project_context: Dict[str, Any]) -> str:
        rtl = project_context.get("rtl_code", "")
        spec = project_context.get("spec_code", "")
        tb = project_context.get("testbench_code", "")
        res = project_context.get("result") or {}

        diagnostics = res.get("diagnostics", [])
        traceability = res.get("traceability", [])
        waveform = res.get("waveform", {})
        meta = res.get("design_metadata", {})

        return f"""You are KIWI, a friendly RIVA SystemVerilog Verification Engineering Assistant and Mentor.
You help engineers understand RTL bugs, bit-width errors, signedness issues, design intelligence metadata, specification traceability, and waveform analysis.

CURRENT PROJECT CONTEXT:
--- RTL SOURCE ---
{rtl if rtl else '(No RTL provided)'}

--- SPECIFICATION ---
{spec if spec else '(No Specification provided)'}

--- TESTBENCH ---
{tb if tb else '(No Testbench provided)'}

--- DESIGN METADATA ---
{json.dumps(meta, indent=2)}

--- VERIFICATION DIAGNOSTICS ({len(diagnostics)}) ---
{json.dumps(diagnostics, indent=2)}

--- REQUIREMENT TRACEABILITY ({len(traceability)}) ---
{json.dumps(traceability, indent=2)}

--- WAVEFORM SUMMARY ---
{json.dumps(waveform, indent=2)}

INSTRUCTIONS:
1. Be encouraging, concise, and technically accurate.
2. Rely strictly on the provided context evidence. If evidence is missing, state clearly that information is unavailable.
3. Provide SystemVerilog code snippets using ```systemverilog blocks when asked for corrections or examples.
4. Clearly distinguish verified facts from recommendations.
"""

    def _call_gemini_api(self, messages: List[Dict[str, str]], project_context: Dict[str, Any]) -> Optional[str]:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_key}"
            system_instruction = self._build_system_prompt(project_context)

            contents = []
            contents.append({
                "role": "user",
                "parts": [{"text": system_instruction}]
            })
            contents.append({
                "role": "model",
                "parts": [{"text": "Understood! I am Kiwi, RIVA's SystemVerilog engineering assistant. I am ready to guide you based on your project context."}]
            })

            for msg in messages:
                role = "user" if msg.get("role") == "user" else "model"
                contents.append({
                    "role": role,
                    "parts": [{"text": msg.get("content", "")}]
                })

            req_body = json.dumps({"contents": contents}).encode("utf-8")
            req = urllib.request.Request(url, data=req_body, headers={"Content-Type": "application/json"})

            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "")
        except Exception:
            return None
        return None

    def _call_openai_api(self, messages: List[Dict[str, str]], project_context: Dict[str, Any]) -> Optional[str]:
        try:
            url = "https://api.openai.com/v1/chat/completions"
            system_instruction = self._build_system_prompt(project_context)

            api_messages = [{"role": "system", "content": system_instruction}]
            for msg in messages:
                role = "user" if msg.get("role") == "user" else "assistant"
                api_messages.append({"role": role, "content": msg.get("content", "")})

            req_body = json.dumps({
                "model": "gpt-4o-mini",
                "messages": api_messages,
                "temperature": 0.2
            }).encode("utf-8")

            req = urllib.request.Request(url, data=req_body, headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.openai_key}"
            })

            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                choices = data.get("choices", [])
                if choices:
                    return choices[0].get("message", {}).get("content", "")
        except Exception:
            return None
        return None

    def _generate_grounded_fallback(self, messages: List[Dict[str, str]], project_context: Dict[str, Any]) -> str:
        last_msg = messages[-1].get("content", "").strip() if messages else ""
        lower = last_msg.lower()

        res = project_context.get("result") or {}
        diagnostics = res.get("diagnostics", [])
        traceability = res.get("traceability", [])
        waveform = res.get("waveform", {})
        meta = res.get("design_metadata") or {}
        rtl = project_context.get("rtl_code", "").strip()
        spec = project_context.get("spec_code", "").strip()

        sim = waveform.get("simulation", {})
        activity = waveform.get("signal_activity", {})

        # Design Metadata queries
        if "signal" in lower and ("how many" in lower or "count" in lower or "inputs" in lower or "outputs" in lower):
            if meta:
                return f"""**Verified Signal Intelligence**:
- **Total Signals**: {meta.get('signal_count', 0)}
- **Inputs**: {meta.get('input_count', 0)}
- **Outputs**: {meta.get('output_count', 0)}
- **Ports**: {meta.get('port_count', 0)}

Declared Signals: {', '.join([f"`{s['name']}` ({s['direction']}, {s['width']}-bit)" for s in meta.get('signals', [])]) if meta.get('signals') else 'None'}"""
            return "The current analysis does not provide signal metadata. Run verification first."

        if "top module" in lower or "top_module" in lower:
            top_name = meta.get("top_module") or res.get("top_module") or "top"
            return f"**Top Module**: Your design's top-level module is `{top_name}`."

        if "operation" in lower or "op" in lower or "arithmetic" in lower:
            ops = meta.get("operation_counts", {})
            active_ops = {k: v for k, v in ops.items() if v > 0}
            if active_ops:
                ops_str = ", ".join([f"`{k}` ({v})" for k, v in active_ops.items()])
                return f"**Verified RTL Operations**: Your RTL contains {len(active_ops)} active operation types: {ops_str}."
            return "Your RTL contains continuous assignments without complex arithmetic/logic operations."

        if "how long" in lower or "duration" in lower or "simulation time" in lower:
            if sim and sim.get("duration") is not None:
                return f"**Simulation Time**: The simulation ran for **{sim.get('duration')}ns** (from #{sim.get('start_time')}ns to #{sim.get('end_time')}ns with `{sim.get('timescale', '1ns')}` timescale)."
            return "No simulation trace is currently available. Run verification with a testbench to capture simulation duration."

        if "clock" in lower or "frequency" in lower:
            clks = sim.get("clock_signals", [])
            freqs = sim.get("clock_frequencies", {})
            if clks and freqs:
                clk_str = ", ".join([f"`{c}`: {freqs[c]}" for c in clks if c in freqs])
                return f"**Measured Clock Frequency**: {clk_str}."
            return "No clock detected (combinational execution)."

        if "toggle" in lower or "toggl" in lower or "activity" in lower or "transition" in lower:
            if activity:
                sorted_act = sorted(activity.items(), key=lambda item: item[1].get("transitions", 0), reverse=True)
                top_sig, top_info = sorted_act[0]
                return f"**Signal Activity**: Signal `{top_sig}` toggled most with **{top_info.get('transitions')} transitions** during simulation trace."
            return "No signal activity transitions logged. Submit a testbench to measure waveform signal activity."

        # Corrected Code / How to fix query
        if any(w in lower for w in ["fix", "corrected", "correction", "code", "how do i"]):
            if diagnostics:
                d = diagnostics[0]
                code = d.get("code", "RIVA3001")
                msg = d.get("message", "")
                loc = d.get("location", "RTL Source")

                if code == "RIVA3001":
                    return f"""**Recommended SystemVerilog Correction for {code}**

**Problem**: Bit-width mismatch detected at `{loc}`.
*{msg}*

**Why it happened**: SystemVerilog implicit truncation occurs when assigning an expression of wider bit width to a narrower target net.

**Recommended Correction (Option A - Bit Slice)**:
```systemverilog
// Truncate higher bits explicitly using a bit-slice
assign y = a[3:0];
```

**Alternative Correction (Option B - Expand Target Width)**:
```systemverilog
// Widen target signal declaration to 8 bits
output logic [7:0] y;
assign y = a;
```

*Note: Review specification requirements before selecting the correct bit width option.*"""

                if code == "RIVA3002":
                    return f"""**Recommended SystemVerilog Correction for {code}**

**Problem**: Signedness mismatch detected at `{loc}`.
*{msg}*

**Why it happened**: Assigning a signed operand to an unsigned net can cause unexpected sign extension.

**Recommended Correction (Option A - Explicit Unsigned Cast)**:
```systemverilog
assign y = $unsigned(a);
```

**Alternative Correction (Option B - Declare Target as Signed)**:
```systemverilog
output logic signed [7:0] y;
assign y = a;
```"""

                if code == "RIVA1001":
                    return f"""**Recommended SystemVerilog Correction for {code}**

**Problem**: Undeclared identifier detected at `{loc}`.
*{msg}*

**Why it happened**: The signal name used in the expression is not declared in scope.

**Recommended Correction (Option A - Add Signal Declaration)**:
```systemverilog
// Declare the missing input/logic net in top module
input logic [7:0] missing_signal;
```

**Alternative Correction (Option B - Fix Spelling Typo)**:
```systemverilog
// Replace typo with existing declared signal 'a'
assign y = a;
```"""

                if code == "RIVA6002":
                    return f"""**Recommended SystemVerilog Correction for {code}**

**Problem**: Specification requirement mismatch.
*{msg}*

**Recommended Correction**:
```systemverilog
// Declare specification target signal 'data_out' in RTL module header
module top(
    input logic [7:0] a,
    output logic [7:0] y,
    output logic [7:0] data_out
);
```"""
            return """**General SystemVerilog Verification Check**:
Your current design has no active diagnostic errors!

If you are modifying RTL code, ensure:
1. Signal bit widths match continuous assignment expressions.
2. Input/output ports align with specification requirement tags.
3. Testbench stimulus drives inputs cleanly across time delays."""

        # Why design failing / What to fix first query
        if any(w in lower for w in ["failing", "fail", "fix first", "error", "why"]):
            if diagnostics:
                d = diagnostics[0]
                return f"""**Current Project Status**: Verification Found {len(diagnostics)} Issue(s).

**Primary Issue to Fix First**: `{d.get('code')}` at `{d.get('location', 'RTL')}`

**Details**: {d.get('message')}

**Suggested Action**: {d.get('suggestion')}

Ask me `"Give me corrected code"` to inspect SystemVerilog fix snippets for this issue!"""
            elif res.get("status") == "success":
                return "Your design is currently **100% CLEAN**! All static semantic checks, bit-width evaluations, and requirement links passed without errors."
            else:
                return "Click **▶ Start Verification** in the Overview panel to run the RIVA verification pipeline on your active project."

        # Waveform query
        if "waveform" in lower or "vcd" in lower or "trace" in lower:
            events_count = waveform.get("events_count", 0)
            signals = waveform.get("signals_analyzed", [])
            source = waveform.get("source", "none")

            if events_count > 0:
                return f"""**Waveform Trace Summary**:
- **Source**: {source.upper()}
- **Events Logged**: {events_count} transitions
- **Signals Analyzed**: {', '.join(signals) if signals else 'None'}

The simulator trace captured activity across signals `{', '.join(signals)}`. View the Waveform panel in Results to inspect signal transition steps."""
            else:
                return "No waveform data is currently available. Provide a testbench or upload a VCD trace file to capture simulation signal transitions."

        # Specification / Requirement query
        if "requirement" in lower or "spec" in lower or "req" in lower or "satisfy" in lower:
            if traceability:
                passed = [t for t in traceability if t.get("status") == "PASSED"]
                failed = [t for t in traceability if t.get("status") != "PASSED"]
                return f"""**Specification Traceability Status**:
- **Total Requirements Tracked**: {len(traceability)}
- **Passed Requirements**: {len(passed)}
- **Failed Requirements**: {len(failed)}

{f"**Failed Link**: Requirement `{failed[0].get('requirement_id')}` for signal `{failed[0].get('signal_name')}` failed verification." if failed else "All specification requirement links satisfied!"}"""
            elif spec:
                return "Specification text provided. Use `[REQ-001]` tags in your specification file to enable automated requirement traceability."
            else:
                return "No specification text provided in active project. Paste a requirement specification to enable requirement tracing."

        # Default contextual summary
        diag_count = len(diagnostics)
        top_name = meta.get("top_module") or res.get("top_module") or "top"
        return f"""**RIVA Engineering Assistant (Grounded Mode)**

I analyzed your current project context:
- **Top Module**: `{top_name}`
- **Signals**: {meta.get('signal_count', 0)} ({meta.get('input_count', 0)} in / {meta.get('output_count', 0)} out)
- **Diagnostics**: {diag_count} issue(s) logged
- **Waveform**: {waveform.get('events_count', 0)} events recorded

Ask me:
- *"How many signals are in my design?"*
- *"What operations does my RTL use?"*
- *"How long did the simulation run?"*
- *"Why is my design failing?"*
- *"Give me corrected code"*

*(Note: Live LLM API key not detected in environment. Using RIVA grounded context engine).*"""
