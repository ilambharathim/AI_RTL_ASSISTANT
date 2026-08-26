# RIVA API Integration

The RIVA frontend integrates with the backend via the FastAPI REST API. The core endpoint exposed to the frontend is `POST /api/analyze`.

## `POST /api/analyze`

Executes the verification engine pipeline, providing diagnostics, traceability, waveform data, AI reasoning, and consolidated reports.

### Request Payload

```json
{
  "rtl_code": "module top(input logic clk, output logic [7:0] data); assign data = 8'hF0; endmodule",
  "spec_code": "[REQ-01]\\nCategory: FUNCTIONAL\\nSignal: data\\nExpected: 8-bit output",
  "testbench_code": "",
  "vcd_content": "$date 2026-08-20 $end..."
}
```

### Response Payload

```json
{
  "status": "success",
  "top_module": "top",
  "diagnostics": [
    {
      "code": "RIVA3001",
      "category": "Width Mismatch",
      "severity": "warning",
      "message": "Width mismatch description.",
      "suggestion": "Update declaration.",
      "location": "design.sv:1:1"
    }
  ],
  "hierarchy": [
    {
      "name": "top",
      "type": "module",
      "children": []
    }
  ],
  "traceability": [
    {
      "requirement_id": "REQ-01",
      "signal_name": "data",
      "expected": "8-bit output",
      "actual": "8 bits",
      "status": "PASSED"
    }
  ],
  "waveform": {
    "status": "success",
    "events_count": 5,
    "signals_analyzed": ["clk", "data"],
    "observations": []
  },
  "explanation": {
    "summary": "AI summary text.",
    "findings": [
      {
        "code": "RIVA3001",
        "location": "design.sv:1:1",
        "explanation": "Detailed explanation.",
        "suggested_fix": "Detailed fix."
      }
    ],
    "confidence_score": 95
  },
  "reports": {
    "markdown": "# RIVA Consolidated Verification Report\n\n**Project**: ...",
    "json": "{\"evidence\": {...}, \"ai_reasoning\": {...}}"
  }
}
```

## Reports Contract

### `reports.markdown`

**Type**: `string`

Backend-generated Markdown report from `ConsolidatedReportGenerator.generate_markdown_report()`.

Content includes:
- Project name and verification status (`PASSED` / `FAILED`)
- Overall AI confidence score
- Executive summary (from AI reasoning engine)
- Diagnostic findings table: code, category, severity, location, message, suggestion
- Specification traceability table: requirement ID, target signal, status, details
- AI grounded explanations and recommended fixes per diagnostic code

The frontend renders this string verbatim using a `<pre>` element. It is **never** rewritten, summarized, or altered by the frontend.

### `reports.json`

**Type**: `string` (serialized JSON from `json.dumps(...)`)

Backend-generated JSON report from `ConsolidatedReportGenerator.generate_json_report()`.

When parsed, the top-level object has two keys:
```json
{
  "evidence": { ... },      // EvidencePayload.to_dict() output
  "ai_reasoning": { ... }   // AIReasoningEngine.generate_explanation() output
}
```

The frontend renders this string verbatim in a monospace code block. It is **never** re-serialized or modified by the frontend. Copy and Download actions export the exact string received from the backend.

## Data Types (TypeScript)

The primary types required by the frontend are maintained in `frontend/src/types/api.ts`:

```typescript
export interface Reports {
  markdown: string;  // Backend-generated Markdown report (verbatim string)
  json: string;      // Backend-generated JSON report (serialized JSON string)
}

export interface AnalyzeResponse {
  status: string;
  top_module: string;
  diagnostics: Diagnostic[];
  hierarchy: HierarchyNode[];
  traceability: TraceabilityLink[];
  waveform: WaveformResult;
  explanation: AIExplanation;
  reports: Reports;
}
```

The frontend does not construct mock payloads and relies entirely on these types and the backend responses.

## Notes

- The frontend does **not** call a separate `/api/report` endpoint. Reports are returned inline with the `POST /api/analyze` response.
- The frontend does **not** generate verification reports. `ConsolidatedReportGenerator` on the backend is the single source of truth.
- `reports.json` is a **string** (not a JSON object) in the HTTP response. The frontend may call `JSON.parse()` to validate it is well-formed, but copies and downloads the original string without modification.
