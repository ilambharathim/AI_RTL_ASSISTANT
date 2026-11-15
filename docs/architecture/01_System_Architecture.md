# 01 - System Architecture

## Overview
**RIVA (RTL Verification and Intelligent Verification Assistant)** is an industrial-grade, AI-assisted SystemVerilog verification and automated bug repair framework. Designed for VLSI and digital design engineers, RIVA bridges the gap between deterministic formal/rule-based RTL linting and Large Language Model (LLM) code generation without hallucination risks.

```
+---------------------------------------------------------------------------------------+
|                                    RIVA Workstation                                   |
|       (React 19 + TypeScript + TailwindCSS + Monaco Editor + Interactive Waveform)     |
+-------------------------------------------+-------------------------------------------+
                                            | REST API (JSON / Multipart)
                                            v
+---------------------------------------------------------------------------------------+
|                                  FastAPI Backend Core                                 |
|                                                                                       |
|   +-----------------------+   +------------------------+   +----------------------+   |
|   |  HDL Lexer & Parser   |-->| Semantic Type & Width  |-->| Diagnostic Catalog   |   |
|   |  (IEEE 1800 Subset)   |   | Inference Engine       |   | (Latches, FSM, Width)|   |
|   +-----------------------+   +------------------------+   +----------------------+   |
|                                                                        |              |
|   +-----------------------+   +------------------------+               v              |
|   | Simulation Harness    |<--| Kiwi AI Provider       |<--+----------------------+   |
|   | (Questa / Vivado / IV)|   | (Grounded Context)     |   | Grounded Evidence    |   |
|   +-----------------------+   +------------------------+   | Store (Deterministic)|   |
|               |                           |                +----------------------+   |
|               v                           v                                           |
|       [ Regression Pass ]     [ Refined Candidate Fix ]                               |
+---------------------------------------------------------------------------------------+
```

## System Subsystems

### 1. Deterministic Analysis Engine
- **AST Construction**: Builds strongly typed AST nodes for SystemVerilog modules, ports, parameters, continuous assignments, procedural blocks (`always`, `always_comb`, `always_ff`), case statements, and conditional expressions.
- **Semantic Type & Width Inference**: Computes precise expression bit-widths, evaluates constant expressions, enforces signedness rules, and catches implicit truncations and extension hazards.
- **Control Flow & Dataflow Graphs**: Constructs basic block CFGs to compute liveness analysis, detect unreachable states, dead assignments, and cyclic combinational loops.

### 2. Closed-Loop Auto-Repair Subsystem
- **Grounded Evidence Store**: Isolates exact AST node coordinates, symbol definitions, and diagnostic codes. The AI fix engine is strictly forbidden from extrapolating beyond verified facts.
- **Candidate Patch Generation**: Synthesizes surgical replacement patches formatted for direct AST substitution or unified line diffs.
- **Simulation Validation Harness**: Compiles and simulates candidate RTL patches against the golden testbench via QuestaSim, Xilinx Vivado, or Icarus Verilog.
- **Feedback Retry Loop**: If simulation fails or produces assertion errors, the failure log is fed back to the LLM for iterative correction up to a bounded retry limit.

### 3. Verification Workstation UI
- **Live Code Editor**: Features Monaco / Ace code views with inline diagnostic markers, line squiggles, and direct patch review.
- **Hierarchical Design Inspector**: Explores module instantiation trees, port declarations, nets, and design metrics.
- **Waveform Canvas**: Inspects `.vcd` timing diagrams, signal transitions, clock cycles, and bus representations.
- **Kiwi Assistant Chat**: Real-time engineering co-pilot grounded in current project AST evidence.
