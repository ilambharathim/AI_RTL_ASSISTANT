# 03 - Data Flow

## End-to-End Execution Pipeline

The execution flow within RIVA follows a deterministic pipeline from source ingestion to simulation-backed auto-repair.

```mermaid
sequenceDiagram
    autonumber
    actor Engineer as VLSI Engineer
    participant UI as RIVA Workstation
    participant API as FastAPI Router
    participant Parser as Lexer / AST Builder
    participant Semantics as Width & Type Engine
    participant Engine as Diagnostic Engine
    participant Trace as Requirement Tracer
    participant Kiwi as Kiwi AI Assistant
    participant Sim as Simulator (Vivado / IV)

    Engineer->>UI: Submit RTL Source + Spec + Testbench
    UI->>API: POST /api/analyze
    API->>Parser: Parse SV Tokens & Construct AST
    Parser-->>API: AST Compilation Unit
    API->>Semantics: Infer Widths & Resolve Scopes
    Semantics-->>API: Annotated Semantic Model
    API->>Engine: Run Diagnostic Rules (Latch, Width, FSM)
    Engine-->>API: List of Diagnostics & Slices
    API->>Trace: Trace Spec Requirements vs RTL
    Trace-->>API: Traceability Matrix (Pass/Gaps)
    API->>Kiwi: Grounded AI Reasoner (Generate Auto-Fix)
    Kiwi-->>API: Candidate Patch Slices
    API->>Sim: Run Simulation Regression on Patched RTL
    alt Simulation Passes
        Sim-->>API: Regression PASS (0 Assertions Failed)
    else Simulation Fails
        Sim-->>API: Regression FAIL (Error Trace)
        API->>Kiwi: Feedback Retry with Sim Error Log
        Kiwi-->>API: Refined Patch Candidate
        API->>Sim: Re-simulate Refined Patch
    end
    API-->>UI: Unified Analysis, Waveforms, Diagnostics & Patches
    UI-->>Engineer: Interactive Visual Results & One-Click Merge
```

## Data Payloads

1. **Request Payload (`/api/analyze`)**:
   - `code`: SystemVerilog HDL source text.
   - `spec`: Markdown / text design specification requirements.
   - `testbench`: Testbench HDL code or VCD trace data.
   - `options`: Severity thresholds, target simulator, and optimization passes.

2. **Analysis Result Payload**:
   - `diagnostics`: Array of categorized bugs with source locations, severity, and rule explanations.
   - `traceability`: Requirement coverage table linking specification paragraphs to RTL module instances.
   - `repairs`: Synthesized patches with code diffs, root-cause explanations, and confidence scores.
   - `waveform`: Signal transitions, timeline bounds, and bus values extracted from testbench VCD.
   - `metadata`: Module counts, port lists, flip-flop registers, and gate metrics.
